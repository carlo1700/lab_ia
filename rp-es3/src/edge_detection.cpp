#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <assert.h>
#include "image.h"

#define M_PI 3.14159265358979323846

void l2_normalize(Image &im) {

    float sum = 0;
    for (int k = 0; k < im.c; k++)
    {
        for (int i = 0; i < im.w; i++)
        {
            for (int j = 0; j < im.h; j++)
                sum += im(i, j, k);
        }
        for (int i = 0; i < im.w; i++)
        {
            for (int j = 0; j < im.h; j++)
                im(i, j, k) /= sum;
        }
    }
}

Image smooth_image(const Image& im, float sigma)
{
    assert (im.c == 1 && "Image is not grayscale");
    Image ret = convolve_image(im, make_gaussian_filter(sigma), 0);

    return ret;
}


pair<Image,Image> compute_gradient(const Image& im)
{

    pair<Image,Image> sobel = sobel_image(im);
    Image mag = sobel.first;
    Image dir = sobel.second;
    feature_normalize(mag);

    return{mag, dir};
}

Image non_maximum_suppression(const Image& mag, const Image& dir)
{
    Image nms(mag.w, mag.h, 1);
    Image angle(mag.w, mag.h, 1);


    for (int y = 0; y < mag.h; y++) {
        for (int x = 0; x < mag.w; x++) {

            angle(x, y, 0) = (dir(x, y, 0) * 180) / M_PI;
            if (angle(x, y, 0) < 0)
                angle(x, y, 0) += 180;
            if (angle(x, y, 0) >= 180)
                angle(x, y, 0) -= 180;
        }
    }


    for (int y = 0; y < mag.h ; y++) {
        for (int x = 0; x < mag.w ; x++) {
            float q = 255;
            float r = 255;

            // angle 0
            if (0 <= angle(x, y, 0) && angle(x, y, 0) < 22.5) {
                q = mag.clamped_pixel(x + 1, y, 0);
                r = mag.clamped_pixel(x - 1, y, 0);
            }
            // angle 45
            else if (22.5 <= angle(x, y, 0) && angle(x, y, 0) < 67.5) {
                q = mag.clamped_pixel(x + 1, y + 1, 0);
                r = mag.clamped_pixel(x - 1, y - 1, 0);
            }
            // angle 90
            else if (67.5 <= angle(x, y, 0) && angle(x, y, 0) < 112.5) {
                q = mag.clamped_pixel(x, y + 1, 0);
                r = mag.clamped_pixel(x, y - 1, 0);
            }
            // angle 135
            else if (112.5 <= angle(x, y, 0) && angle(x, y, 0) < 157.5) {
                q = mag.clamped_pixel(x - 1, y + 1, 0);
                r = mag.clamped_pixel(x + 1, y - 1, 0);
            }
            // angle 180
            else if (157.5 <= angle(x, y, 0) && angle(x, y, 0) <= 180) {
                q = mag.clamped_pixel(x - 1, y, 0);
                r = mag.clamped_pixel(x + 1, y, 0);
            }

            if ((mag(x, y, 0) >= q) && (mag(x, y, 0) >= r)) {
                nms(x, y, 0) = mag(x, y, 0);
            }
            else {
                nms(x, y, 0) = 0;
            }

        }
    }
    return nms;
}

// classifica i pixel in forti, deboli e non rilevanti
Image double_thresholding(const Image& im, float lowThreshold, float highThreshold, float strongVal, float weakVal)
{
    Image res(im.w, im.h, im.c);

    for (int y=0; y < im.h; ++y) {
        for (int x=0; x < im.w; ++x) {
            if (im(x, y, 0) > highThreshold)
                res(x, y, 0) = strongVal;
            else if (im(x, y, 0) < lowThreshold)
                res(x, y, 0) = 0;
            else
                res(x, y, 0) = weakVal;
        }
    }

    return res;
}


// se un pixel debole è adiacente ad un pixel forte, allora diventa forte
Image edge_tracking(const Image& im, float weak, float strong)
{
    Image res(im.w, im.h, im.c);

    for (int y=0; y < im.h; ++y) {
        for (int x=0; x < im.w; ++x) {
            res(x, y, 0) = im(x, y, 0);
        }
    }

    for (int y=0; y < im.h ; ++y) {
        for (int x=0; x < im.w ; ++x) {
            if (im(x, y, 0) == weak) {
                if ((im.clamped_pixel(x + 1, y, 0) == strong) || (im.clamped_pixel(x - 1, y, 0) == strong) ||
                    (im.clamped_pixel(x, y + 1, 0) == strong) || (im.clamped_pixel(x, y - 1, 0) == strong) ||
                    (im.clamped_pixel(x + 1, y + 1, 0) == strong) || (im.clamped_pixel(x - 1, y - 1, 0) == strong) ||
                    (im.clamped_pixel(x + 1, y - 1, 0) == strong) || (im.clamped_pixel(x - 1, y + 1, 0) == strong))
                    res(x, y, 0) = strong;
                else
                    res(x, y, 0) = 0;
            }
        }
    }
    return res;

}
