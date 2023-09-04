#include <cmath>
#include "image.h"

using namespace std;

// HW1 #1
// float x,y: inexact coordinates
// int c: channel
// returns the nearest neighbor to pixel (x,y,c)
float Image::pixel_nearest(float x, float y, int c) const
{

	int x1, y1;

	x1 = (int) round(x); // arrotonda x
	y1 = (int) round(y); // arrotonda y

	return clamped_pixel(x1, y1, c);
}



// HW1 #1
// float x,y: inexact coordinates
// int c: channel
// returns the bilinearly interpolated pixel (x,y,c)
float Image::pixel_bilinear(float x, float y, int c) const
{
	float x1, y1, x2, y2;
	// trova intero piu piccolo e piu grande vicino a x e y
	x1 = floor(x);
	y1 = floor(y);
	x2 = ceil(x);
	y2 = ceil(y);

	// trova i valori dei pixel vicini
	float q11, q12, q21, q22;
	q11 = clamped_pixel(x1, y1, c);
	q12 = clamped_pixel(x1, y2, c);
	q21 = clamped_pixel(x2, y1, c);
	q22 = clamped_pixel(x2, y2, c);

	//    |-------|-------|
	// y1 |  q11  |  q21  |
	// y  |-----0---------|
	// y2 |  q12  |  q22  |
	//    |-------|-------|
	//       x1   x   x2

	// combina i valori dei pixel vicini per ottenere il valore del pixel (x,y) via interpolazione bilineare
	float q1, q2;
	q1 = q21  * (x - x1) + q11 * (x2 - x);
	q2 = q22 * (x - x1) + q12 * (x2 - x);
	float pixel = q2 * (y - y1) + q1 * (y2 - y);
	return pixel;
}

// HW1 #1
// int w,h: size of new image
// const Image& im: input image
// return new Image of size (w,h,im.c)
Image nearest_resize(const Image& im, int w, int h)
{
	Image ret(w, h, im.c);

	float w_ratio = (float)im.w / w;
    float h_ratio = (float)im.h / h;

	float x, y;

	for (int i = 0; i < w; i++)
	{
		for (int j = 0; j < h; j++)
		{
			x = i * w_ratio + (0.5 * w_ratio - 0.5); // per centrare il pixel
          	y = j * h_ratio + (0.5 * h_ratio - 0.5);

			for (int k = 0; k < im.c; k++)
				ret(i, j, k) = im.pixel_nearest(x, y, k);
		}
	}
	return ret;
}


// HW1 #1
// int w,h: size of new image
// const Image& im: input image
// return new Image of size (w,h,im.c)
Image bilinear_resize(const Image& im, int w, int h)
{
	Image ret(w, h, im.c);

	float w_ratio = (float)im.w / w;
    float h_ratio = (float)im.h / h;

	float x, y;

	for (int i = 0; i < w; i++)
	{
		for (int j = 0; j < h; j++)
		{
			x = i * w_ratio + (0.5 * w_ratio - 0.5);
          	y = j * h_ratio + (0.5 * h_ratio - 0.5);

			for (int k = 0; k < im.c; k++)
				ret(i, j, k) = im.pixel_bilinear(x, y, k);
		}
	}
	return ret;
}



