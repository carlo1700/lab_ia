#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <assert.h>
#include<iostream>

#include "image.h"

#define M_PI 3.14159265358979323846

void l1_normalize(Image &im) {

    //normalize the image so that the sum of all the pixels is 1

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

Image make_box_filter(int w) {
    assert(w % 2); // w needs to be odd // pari
	Image filter = Image(w, w, 1);
    for (int i = 0; i < w; i++)
    {
        for (int j = 0; j < w; j++)
            filter(i, j, 0) = 1.0 / (w * w);
    }
    return filter;
}

Image convolve_image(const Image &im, const Image &filter, bool preserve) {
    assert(filter.c == 1);
    Image ret = Image(im.w, im.h, preserve ? im.c : 1);
	float q = 0;
	int filter_offest = filter.w / 2;

    for (int i = 0; i < im.w; i++)
    {
        for (int j = 0; j < im.h; j++)
        {
            if (preserve)
            {
                for (int k = 0; k < im.c; k++)
                {
                    q = 0;
				    for (int x = -filter_offest; x <= filter_offest ; x++)
                    {
					    for (int y = -filter_offest; y <= filter_offest ; y++)
                        {
						    float a = im.clamped_pixel(i - x, j - y, k);
                            float b = filter(filter_offest - x, filter_offest - y);
                            q += a * b;
				        }
                    }
				    ret(i, j, k) = q;
                }
            }
            else
            {
                q = 0;
                for (int x = -filter_offest; x <= filter_offest; x++)
                {
                    for (int y = -filter_offest; y <= filter_offest; y++)
                    {
                        for (int k = 0; k < im.c; k++)
                        {
                            float a = im.clamped_pixel(i - x, j - y, k);
                            float b = filter(filter_offest - x, filter_offest - y);
                            q += a * b;
                        }
                    }
                }
                ret(i, j, 0) = q;
            }
        }
    }
    return ret;
}


Image convolve_image_fast(const Image &im, const Image &filter, bool preserve) {
    assert(filter.c == 1);
    Image ret;
    // This is the case when we need to use the function clamped_pixel(x,y,c).
    // Otherwise you'll have to manually check whether the filter goes out of bounds

    // TODO: Make sure you set the sizes of ret properly. Use ret=Image(w,h,c) to reset ret
    // TODO: Do the fast convolution operator. Remember to use Eigen for matrix operations
    NOT_IMPLEMENTED();

    // Make sure to return ret and not im. This is just a placeholder
    return im;
}


Image make_highpass_filter() {
    Image filter = Image(3, 3, 1);
    float filter_data[3][3] = {{0, -1, 0},
                               {-1, 4, -1},
                               {0, -1, 0}};
    float normalizer = 1.0;
    for (int i = 0; i < 3; i++)
    {
        for (int j = 0; j < 3; j++)
            filter(i, j, 0) = filter_data[i][j] * normalizer;
    }
    return filter;

}

Image make_sharpen_filter() {
    Image filter = make_box_filter(3);
    filter(0, 0, 0) = 0;
    filter(0, 1, 0) = -1;
    filter(0, 2, 0) = 0;
    filter(1, 0, 0) = -1;
    filter(1, 1, 0) = 5;
    filter(1, 2, 0) = -1;
    filter(2, 0, 0) = 0;
    filter(2, 1, 0) = -1;
    filter(2, 2, 0) = 0;
    return filter;

    // 0 -1 0
    // -1 5 -1
    // 0 -1 0
}

// HW1 #2.3
// returns basic 3x3 emboss filter 3D
Image make_emboss_filter() {
    Image filter = make_box_filter(3);
    filter(0, 0, 0) = -2;
    filter(0, 1, 0) = -1;
    filter(0, 2, 0) = 0;
    filter(1, 0, 0) = -1;
    filter(1, 1, 0) = 1;
    filter(1, 2, 0) = 1;
    filter(2, 0, 0) = 0;
    filter(2, 1, 0) = 1;
    filter(2, 2, 0) = 2;
    return filter;

    // -2 -1 0
    // -1 1 1
    // 0 1 2
}

Image make_gaussian_filter(float sigma) {
    int kernel_size = 6 * sigma;
    if (kernel_size % 2 == 0)
        kernel_size += 1;
    Image filter = Image(kernel_size, kernel_size, 1);
    float normalizer = 0;
    for (int i = 0; i < kernel_size; i++)
    {
        for (int j = 0; j < kernel_size; j++)
        {
            float x = i - kernel_size / 2;
            float y = j - kernel_size / 2;
            float value = exp(-(x * x + y * y) / (2 * sigma * sigma));
            filter(i, j, 0) = value;
            normalizer += value;
        }
    }
    for (int i = 0; i < kernel_size; i++)
    {
        for (int j = 0; j < kernel_size; j++)
        {
            filter(i, j, 0) /= normalizer;
        }
    }
    return filter;
}

Image add_image(const Image &a, const Image &b) {
    assert(a.w == b.w && a.h == b.h && a.c == b.c); // assure images are the same size

    Image ret = Image(a.w, a.h, a.c);
    for (int i = 0; i< a.w; i++)
    {
        for (int j = 0; j < a.h; j++)
        {
            for (int k = 0; k < a.c; k++)
            {
                ret(i, j, k) = a(i, j, k) + b(i, j, k);
            }
        }
    }

    return ret;
}

Image sub_image(const Image &a, const Image &b) {
    assert(a.w == b.w && a.h == b.h &&
           a.c == b.c); // assure images are the same size

    Image ret = Image(a.w, a.h, a.c);
    for (int i = 0; i< a.w; i++)
    {
        for (int j = 0; j < a.h; j++)
        {
            for (int k = 0; k < a.c; k++)
            {
                ret(i, j, k) = a(i, j, k) - b(i, j, k);
            }
        }
    }

    return ret;
}

// HW1 #4.1
// returns basic GX filter
Image make_gx_filter()
{
    Image filter = Image(3, 3, 1);
    filter(0, 0, 0) = -1;
    filter(1, 0, 0) = 0;
    filter(2, 0, 0) = 1;
    filter(0, 1, 0) = -2;
    filter(1, 1, 0) = 0;
    filter(2, 1, 0) = 2;
    filter(0, 2, 0) = -1;
    filter(1, 2, 0) = 0;
    filter(2, 2, 0) = 1;

    return filter;
}

// HW1 #4.1
// returns basic GY filter
Image make_gy_filter()
  {

    Image filter = Image(3, 3, 1);
    filter(0, 0, 0) = -1;
    filter(1, 0, 0) = -2;
    filter(2, 0, 0) = -1;
    filter(0, 1, 0) = 0;
    filter(1, 1, 0) = 0;
    filter(2, 1, 0) = 0;
    filter(0, 2, 0) = 1;
    filter(1, 2, 0) = 2;
    filter(2, 2, 0) = 1;

    return filter;
  }

float Min(float a, float b)
{
    if (a < b) return a;
    else return b;
}

float Max(float a, float b)
{
    if (a > b) return a;
    else return b;
}

// HW1 #4.2
// Image& im: input image
void feature_normalize(Image &im) {
    assert(im.w * im.h); // assure we have non-empty image

    for (int c = 0; c < im.c; c++)
    {
        float min = im(0, 0, c);
        float max = im(0, 0, c);
        for (int i = 0; i < im.w; i++)
        {
            for (int j = 0; j < im.h; j++)
            {
                float temp = im(i, j, c);
                min = Min(min, temp);
                max = Max(max, temp);
            }
        }
        float range = max - min;

        for (int i = 0; i < im.w; i++)
        {
            for (int j = 0; j < im.h; j++)
            {
                if (range == 0) im(i, j, c) = 0;
                else im(i, j, c) = (im(i, j, c) - min) / range;
            }
        }
    }
}


// Normalizes features across all channels
void feature_normalize_total(Image &im) {
    assert(im.w * im.h * im.c); // assure we have non-empty image

    int nc = im.c;
    im.c = 1;
    im.w *= nc;

    feature_normalize(im);

    im.w /= nc;
    im.c = nc;

}


pair<Image, Image> sobel_image(const Image &im) {
    // TODO: Your code here
    Image fx = make_gx_filter();
    Image fy = make_gy_filter();

    Image Gx = convolve_image (im, fx, false);
    Image Gy = convolve_image (im, fy, false);

    Image G(im.w, im.h, 1); // ampiezza del gradiente
    Image T(im.w, im.h, 1); // direzione del gradiente

    for (int y = 0; y < im.h; y ++) {
        for (int x = 0; x < im.w; x ++) {
            G(x,y,0) = sqrtf ( pow(Gx(x,y,0), 2) + pow(Gy(x,y,0), 2));
            T(x,y,0) = atan2f( Gy(x,y,0) , Gx(x,y,0));
        }
    }
    return {G,T};
}


// HW1 #4.4
// const Image& im: input image
// returns the colorized Sobel image of the same size
Image colorize_sobel(const Image &im) {
// TODO: Your code here
    Image gf = make_gaussian_filter(4);
    Image blur = convolve_image(im, gf, true);
    blur.clamp();

    pair<Image, Image> sobel = sobel_image(blur);
    Image mag = sobel.first;
    Image theta = sobel.second;

    feature_normalize(mag);

    // normalizzo theta
    for (int i = 0; i< im.w; i++)
    {
        for (int j = 0; j < im.h; j++)
        {
            theta(i, j, 0) = theta(i, j, 0) / (2 * M_PI) + 0.5;
        }
    }

    Image hsv(im.w, im.h, 3);

    for (int i = 0; i< im.w; i++)
    {
        for (int j = 0; j < im.h; j++)
        {
            hsv(i, j, 0) = theta(i, j, 0);
            hsv(i, j, 1) = mag(i, j, 0);
            hsv(i, j, 2) = mag(i, j, 0);
        }
    }

    hsv_to_rgb(hsv);

    //NOT_IMPLEMENTED();

    return hsv;
}


Image make_bilateral_filter(const Image &im, const Image &gf, int x, int y, int c, float sigma2)
{
	Image cgf(gf.w, gf.h, 1);

	for (int i = 0; i < cgf.w; i++)
	{
		for (int j = 0; j < cgf.h; j++)
		{
			int ax = x - cgf.w / 2 + i;
			int ay = y - cgf.h / 2 + j;

			float diff = im.clamped_pixel(ax, ay, c) - im.clamped_pixel(x, y, c); // differenza di intensità

			float var = powf (sigma2, 2);
			float coef = 2 * var * M_PI;
			float p = - powf(diff, 2) / (2 * var);
			float e = expf (p);
			float val = e / coef;
			cgf(i, j, 0) = val;
		}
	}

	Image bilateralFilter(gf.w, gf.h, 1);

	for (int i = 0; i < bilateralFilter.w; i++)
	{
		for (int j = 0; j < bilateralFilter.h; j++)
		{
			bilateralFilter(i, j, 0) = cgf(i, j, 0) * gf(i, j, 0); // spaziale e intensità
		}
	}

	l1_normalize(bilateralFilter);
	return bilateralFilter;
}

// HW1 #4.5
// const Image& im: input image
// float sigma1,sigma2: the two sigmas for bilateral filter
// returns the result of applying bilateral filtering to im
Image bilateral_filter(const Image &im, float sigma1, float sigma2) {

    // TODO: Your bilateral code
    //NOT_IMPLEMENTED();
	Image gf = make_gaussian_filter(sigma1);

	Image ret(im.w, im.h, im.c);

	for (int c = 0; c < im.c; c++)
	{
		for (int y = 0; y < im.h; y++)
		{
			for (int x = 0; x < im.w; x++)
			{
				Image bilateralFilter = make_bilateral_filter(im, gf, x, y, c, sigma2);

				float sum = 0.0;

				for (int i = 0; i < gf.w; i++) // da -k a +k con kernel di dimensione 2k+1
				{
					for (int j = 0; j < gf.h; j++) // da -k a +k con kernel di dimensione 2k+1
					{
						int ax = x - bilateralFilter.w / 2 + i;
						int ay = y - bilateralFilter.h / 2 + j;
						sum += im.clamped_pixel(ax, ay, c) * bilateralFilter(i, j, 0);
					}
				}
				ret (x, y, c) = sum;
			}
		}
	}
    return ret;
}

// HW1 #4.5+ Fast bilateral filter
// const Image& im: input image
// float sigma1,sigma2: the two sigmas for bilateral filter
// returns the result of applying bilateral filtering to im
Image bilateral_filter_fast(const Image &im, float sigma1, float sigma2) {
    Image bf = im;

    // TODO: Your fast bilateral code
    NOT_IMPLEMENTED();

    return bf;
}

// HM #5
// bin = intervallo di valori
// per un solo canale
float *compute_histogram(const Image &im, int ch, int num_bins) {

    float *histogram = (float *) malloc(sizeof(float) * num_bins);

    for (int i = 0; i < num_bins; ++i)
        histogram[i] = 0;

	int binNum;
    int numPixel = im.w * im.h;
    float eps = 1.0 / (num_bins * 1000); // per evitare problemi di approssimazione

    for (int i = 0; i < im.w; i++)
    {
        for (int j = 0; j < im.h; j++)
        {
            binNum = (int)((im(i, j, ch) - eps) * num_bins);
            histogram[binNum]++;
        }
    }
    for (int i = 0; i < num_bins; i++)
        histogram[i] /= numPixel;

    return histogram;
}

float *compute_CDF(float *hist, int num_bins) {
    float *cdf = (float *) malloc(sizeof(float) * num_bins);

    cdf[0] = hist[0];

	for (int i = 1; i < num_bins; i++)
		cdf[i] = cdf[i - 1] + hist[i];

    return cdf;
}

Image histogram_equalization_hsv(const Image &im, int num_bins) {
    Image new_im(im);
    float eps = 1.0 / (num_bins * 1000);

    // convert to hsv
    rgb_to_hsv(new_im);

    float *histogram = compute_histogram(new_im, 2, num_bins);

    float *cdf = compute_CDF(histogram, num_bins);

    //rgb_to_hsv(new_im);

    for(int i = 0; i < new_im.w; i++) {
        for(int j = 0; j < new_im.h; j++) {
            unsigned int val = (unsigned int) ((new_im(i, j, 2) - eps) * num_bins);
            new_im(i, j, 2) = cdf[val];
        }
    }

    hsv_to_rgb(new_im);
    delete histogram;
    delete cdf;

    return new_im;
}

Image histogram_equalization_rgb(const Image &im, int num_bins) {
    Image new_im(im);
    float eps = 1.0 / (num_bins * 1000);

    for (int c = 0; c < im.c; ++c) {
        float *histogram = compute_histogram(new_im, c, num_bins);
        float *cdf = compute_CDF(histogram, num_bins);

        for(int i = 0; i < new_im.w; i++) {
            for(int j = 0; j < new_im.h; j++) {
                unsigned int val = (unsigned int) ((new_im(i, j, c) - eps) * num_bins);
                new_im(i, j, c) = cdf[val];
            }
        }
        delete histogram;
        delete cdf;
    }

    return new_im;
}


// HELPER MEMBER FXNS

void Image::feature_normalize(void) { ::feature_normalize(*this); }

void Image::feature_normalize_total(void) { ::feature_normalize_total(*this); }

void Image::l1_normalize(void) { ::l1_normalize(*this); }

Image operator-(const Image &a, const Image &b) { return sub_image(a, b); }

Image operator+(const Image &a, const Image &b) { return add_image(a, b); }
