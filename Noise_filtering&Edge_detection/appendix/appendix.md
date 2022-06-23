# Appendix
## cvector Class `cvector<type>`
The cvector class is a vector with special functions and operations.
We overloaded the basic operations in order to be compatable with the cvector now we can do the following in jus one line of code :
- add a scaler value to the cvector : `cvector + 2` -> this will add 2 to each element 
- add two cvectors  : `cvector1 + cvector2` -> this will add each element together 
- substract a scaler value from the cvector  : `cvector1 - 2` -> this will substract 2 from each element  
- substract two cvectors  : `cvector1 - cvector2` -> this will substract each element
- multiply a scaler value to the cvector : `cvector * 2` -> this will multiply 2 to each element 
- multiply two cvectors  : `cvector1 * cvector2` -> this will multiply each element together 
- divide cvector by scaler value : `cvector / 2` -> this will divide each element / 2 
- divide two cvectors  : `cvector1 / cvector2` -> this will divide each element by the corresponding element

We added some useful functions to the cvector class 
- `dot(const cvector<T> &v)` -> this function will perform a dot product
- `mean(void)` -> this will get the mean value for the elements
- `median(void)` -> this will get the median value for the elements

Last thing we want to introduce that you can print out the elements of the cvector by just perform `std::cout << cvector1 ` this will print out the folowings `{el1,el2,el3}`

## Image Class `Image`
In this class, we used the powerfull tool that we developed `cvector<>` with the `Mat` dataType from the openCV to Create the Image class that holds functions to perform different kind of imaging techniques. 
this class has three constructors : 
- `Image::Image(std::string path)` -> this takes the image path 
- `Image::Image(cvector<uchar> pixels, size_t rows, size_t cols, int type)` -> this takes the image as a cvector
- `Image::Image(cv::Mat mat)` this takes a Mat dataType

### Image methods
| Methods | description | 
|:-------|:------------|
| `Image::display(std::string txt)` | this displays the Image  | 
| `Image::vectorize()` | this will turn the image to 1-D cvector stored at the pixels variable | 
| `cvector<cvector<uchar>> Image::to_2d()` | returns 2d cvector with the pixels  |
| `Image filter(const Image &img, cvector<cvector<uchar>> mask)` | this function apply specific kernel to an image|
