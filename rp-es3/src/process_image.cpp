#include <cstdio>
#include <cstring>
#include <cassert>
#include <cmath>

#include "image.h"

using namespace std;

// HW0 #3
// const Image& im: input image
// return the corresponding grayscale image
Image rgb_to_grayscale(const Image& im)
{
	assert(im.c == 3); // only accept RGB images
	Image gray(im.w,im.h,1); // create a new grayscale image (note: 1 channel)
	// TODO: calculate the pixels of 'gray'
	//NOT_IMPLEMENTED();
	int i = 0;
	float Y = 0;
	while (i < im.w * im.h)
	{
		Y = im.data[i] * 0.299;
		Y += im.data[i + im.w * im.h] * 0.587;
		Y +=  im.data[i + im.w * im.h * 2] * 0.114;
		gray.data[i] = Y;

		i++;
	}
	return gray;
}



// Example function that changes the color of a grayscale image
Image grayscale_to_rgb(const Image& im, float r, float g, float b)
  {
  assert(im.c == 1);
  Image rgb(im.w,im.h,3);

  for(int q2=0;q2<im.h;q2++)for(int q1=0;q1<im.w;q1++)
    {
    rgb(q1,q2,0)=r*im(q1,q2);
    rgb(q1,q2,1)=g*im(q1,q2);
    rgb(q1,q2,2)=b*im(q1,q2);
    }

  return rgb;
  }


// HW0 #4
// Image& im: input image to be modified in-place
// int c: which channel to shift
// float v: how much to shift
void shift_image(Image& im, int c, float v)
{
	assert(c>=0 && c<im.c); // needs to be a valid channel

	// TODO: shift all the pixels at the specified channel
	int i = 0;
	//printf("c:%d-",c);
	//printf("w:%d-",im.w);
	//printf("h:%d\n",im.h);

	while (i < im.w * im.h * (c + 1))
	{
		if (i >= im.w * im.h * c)
		{
			//if (i %10000 == 0)
			//	printf("[i:%d]: %f -> %f)\n", i, im.data[i], im.data[i] + v);
			im.data[i] = im.data[i] + v;
		}
		i++;
	}
	//NOT_IMPLEMENTED();
}

// HW0 #8
// Image& im: input image to be modified in-place
// int c: which channel to scale
// float v: how much to scale
void scale_image(Image& im, int c, float v)
  {
  assert(c>=0 && c<im.c); // needs to be a valid channel

  // TODO: scale all the pixels at the specified channel

  	int i = 0;
	while (i < im.w * im.h * (c + 1))
	{
		if (i >= im.w * im.h * c)
			im.data[i] *= v;
		i++;
	}

	/*
	while (im.data[i])
	{
		if (i >= im.w * im.h * c && i < im.w * im.h * (c + 1))
			im.data[i] -= v;
		i++;
	}
	*/
  }


// HW0 #5
// Image& im: input image to be modified in-place
void clamp_image(Image& im)
  {
  // TODO: clamp all the pixels in all channel to be between 0 and 1

	for (int i = 0; i < im.w; i++)
	{
		for (int j = 0; j < im.h; j++)
		{
			for (int k = 0; k < im.c; k++)
			{
				if (im(i, j, k) < 0)
					im(i, j, k) = 0;
				else if (im(i, j, k) > 1)
					im(i, j, k) = 1;
			}
		}
	}


  //NOT_IMPLEMENTED();
  }

// These might be handy
float max(float a, float b, float c)
  {
  return max({a,b,c});
  }

float min(float a, float b, float c)
  {
  return min({a,b,c});
  }


// HW0 #6
// Image& im: input image to be modified in-place
void rgb_to_hsv(Image& im)
{
  assert(im.c==3 && "only works for 3-channels images");

  // TODO: Convert all pixels from RGB format to HSV format

  //NOT_IMPLEMENTED();
  float V;
  float m, C, S;
  float R, G, B;
  float H1 , H;
	//printf ("w:%d - ", im.w);
	//printf ("h:%d\n", im.h);
  int i = 0;
  while (i < im.w * im.h)
  {
	R = im.data[i];
	G = im.data[i + (im.w * im.h)];
	B = im.data[i + (im.w * im.h * 2)];

	//if (i % 10000 == 0 || i == 5073)
	//	printf("%d-R,G,B: %f %f %f ---> ",i,R,G,B);

	V = max(R, G, B);
	m = min(R, G, B);
	C = V - m;
	if (V == 0)
		S = 0;
	else
		S = C / V;
	if (C == 0)
		H = 0;
	else
	{
		if (V == R)
			H1 = (G - B) / C;
		else if (V == G)
			H1 = ((B - R) / C ) + 2;
		else if (V == B)
			H1 = ((R - G) / C) + 4;
		if (H1 < 0)
			H = (H1 / 6) + 1;
		else
			H = H1 / 6;
	}
	if (H < 0)
		H += 1;
	else if (H >= 1)
		H -= 1;
	im.data[i] = H;
	im.data[i + (im.w * im.h)] = S;
	im.data[i + (im.w * im.h * 2)] = V;
	//if (i % 10000 == 0 || i == 5073)
	//	printf("H,S,V: %f %f %f\n",H,S,V);
	i++;
  }
}

// HW0 #7
// Image& im: input image to be modified in-place
void hsv_to_rgb(Image& im)
{
  assert(im.c==3 && "only works for 3-channels images");

  // TODO: Convert all pixels from HSV format to RGB format

  //NOT_IMPLEMENTED();
	//printf ("w:%d - ", im.w);
	//printf ("h:%d\n", im.h);

  float V, m, C, S;
  float R, G, B;
  float R1, G1, B1;
  float H1, H;
  float X;

  int i = 0;
  while (i < im.w * im.h)
  {
	H = im.data[i];
	S = im.data[i + (im.w * im.h)];
	V = im.data[i + (im.w * im.h * 2)];

	//if (i % 10000 == 0)
	//	printf("%d-H,S,V: %f %f %f ---> ",i,H,S,V);
	// Given the H, S, V channels of an image:
	C = V * S;
	X = C * (1 - abs(fmod(6*H, 2) - 1));
	m = V - C;
	if (H >= 0 && H < 1.0 / 6.0)
	{
		R1 = C;
		G1 = X;
		B1 = 0;
	}
	else if (H >= 1.0 / 6.0 && H < 2.0 / 6.0)
	{
		R1 = X;
		G1 = C;
		B1 = 0;
	}
	else if (H >= 2.0 / 6.0 && H < 0.5)
	{
		R1 = 0;
		G1 = C;
		B1 = X;
	}
	else if (H >= 3.0 / 6.0 && H < 4.0 / 6.0)
	{
		R1 = 0;
		G1 = X;
		B1 = C;
	}
	else if (H >= 4.0 / 6.0 && H < 5.0 / 6.0)
	{
		R1 = X;
		G1 = 0;
		B1 = C;
	}
	else if (H >= 5.0 / 6.0 && H < 1)
	{
		R1 = C;
		G1 = 0;
		B1 = X;
	}

	R = R1 + m;
	G = G1 + m;
	B = B1 + m;

	im.data[i] = R;
	im.data[i + (im.w * im.h)] = G;
	im.data[i + (im.w * im.h * 2)] = B;
	//if (i % 10000 == 0)
	//	printf("R,G,B: %f %f %f\n",R,G,B);
	i++;
  }
}

// HW0 #9
// Image& im: input image to be modified in-place
void rgb_to_lch(Image& im)
  {
  assert(im.c==3 && "only works for 3-channels images");

  // TODO: Convert all pixels from RGB format to LCH format


  NOT_IMPLEMENTED();

  }

// HW0 #9
// Image& im: input image to be modified in-place
void lch_to_rgb(Image& im)
  {
  assert(im.c==3 && "only works for 3-channels images");

  // TODO: Convert all pixels from LCH format to RGB format

  NOT_IMPLEMENTED();

  }



// Implementation of member functions
void Image::clamp(void) { clamp_image(*this); }
void Image::shift(int c, float v) { shift_image(*this,c,v); }
void Image::scale(int c, float v) { scale_image(*this,c,v); }

void Image::HSVtoRGB(void) { hsv_to_rgb(*this); }
void Image::RGBtoHSV(void) { rgb_to_hsv(*this); }
void Image::LCHtoRGB(void) { lch_to_rgb(*this); }
void Image::RGBtoLCH(void) { rgb_to_lch(*this); }
