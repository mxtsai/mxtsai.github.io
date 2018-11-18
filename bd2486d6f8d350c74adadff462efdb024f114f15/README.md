# Sheba Research

## Current Ideas on Mind
 * Maybe apply Gradient Boost for classification stage (similar to DeepLung)?
 * Extend research to include also segmentation (inspired by Deeplung)?
 * How to fix the issue of differerent tumor sizes? 

## Good Papers
### Applied Techniques
* [DeepLung: Deep 3D Dual Path Nets for Automated Pulmonary Nodule Detection and Classification](https://drive.google.com/open?id=13Kc2vb4fSFRDJItY3VJELYAlEnUFwqRi)
  * Keywords: Dual Path Network (DPN), Gradient Boosting Machines (GBM), U-Nets
  * Design: uses CT scans, has both segmentation and classification stage
  
  
* [Multi Modal Convolutional Neural Networks for Brain Tumor Segmentation](https://drive.google.com/open?id=1t6cmvZ3wQs3qEuQ-NVLhz05l7WecLxiq)
  * Late convolution fusion layer works better than sum or max fusion
  
* [Fusion of deep learning models of MRI scans, Mini–Mental State Examination, and logical memory test enhances diagnosis of mild cognitive impairment](https://drive.google.com/open?id=13Nhzs9Q_c0ObVP78CLpS0aAsSztltekF)
  * Took the 3D MRI and grouped the slices into categories. Then selected 3 slices that are similar between each patient and trained a 2D CNN using transfer learning on each 2D slice.  
  * Incorporated other non-image tests (like BIRADS) and built a SVM using that for prediction.
  * Used majority vote of the the MRI and test's SVM to predict result
  * **Problem:** : Unsure if tumor can be categorized as such, need more information on breast cancer to select such slices 

### Network Architectures
* [Dual Path Networks](https://drive.google.com/open?id=1jp28JAsvcatX4g7BSXkHxY1-Yrihszcr)
  * Keywords: ResNet, DenseNet, HORNN (Higher Order RNN)
  * Design: resuses features, and can explore new features


## Interesting Papers (not read yet)
* [Wavelet Convolutional Network](https://arxiv.org/pdf/1805.08620.pdf)
* [Few-shot 3D Multi-modal Medical Image Segmentation using Generative Adversarial Learning](https://arxiv.org/pdf/1810.12241.pdf) (few training sets, addresses multi-modal)
* [Accurate Pulmonary Nodule Detection in Computed Tomography Images Using Deep Convolutional Neural Networks](https://drive.google.com/open?id=1bTGA9gkvhQwZxSwFSaf9aS-IYrgt27ZQ) (has a network to reduce false positives)
* [Segmentation of the Proximal Femur from MR Images using Deep Convolutional Neural Networks](https://drive.google.com/file/d/15nxOf2YbY07wNSF6bXI0oU_Ss6-NNFtH/view?usp=sharing)
 **Multi-Modal Papers**
  * [Dense Multi-path U-Net for Ischemic Stroke Lesion Segmentation in Multiple Image Modalities](https://arxiv.org/pdf/1810.07003.pdf)


## Supplement Information

* Understanding **Gradient Boost** > [*link*](http://www.cse.chalmers.se/~richajo/dit865/files/gb_explainer.pdf) 
* **Wavelets** (Transform) Introduction [*link*](http://dsp.vscht.cz/hostalke/upload/WaveletTransform_Lecture.pdf)

* **Course on Machine Learning** > [*Official Site*](https://mlcourse.ai) and [*Lecture Videos*](https://www.youtube.com/watch?v=QKTuw4PNOsU&list=PLVlY_7IJCMJeRfZ68eVfEcu-UcN9BbwiX)  
   - Includes topic on Random Forest, Ensembles, Gradient Boosting   
* **Introduction to Generative Adversarial Networks**> [*Orielly*](https://www.oreilly.com/learning/generative-adversarial-networks-for-beginners?fbclid=IwAR3WT8qgsc4caZNx5sFccURW5YZ9DEL0BHfUEtIQ2KpQw5lmFCW8yuJ8VJ0)  

### Good Links to Medical Imaging Paper
1. [https://github.com/albarqouni/Deep-Learning-for-Medical-Applications](https://github.com/albarqouni/Deep-Learning-for-Medical-Applications
)

## Not-So-Good Papers
* [Identification and classification of brain tumor MRI images with feature extraction using DWT and probabilistic neural network](https://drive.google.com/open?id=1McJaVlM7YtMVwom4M2ODEPcf9h-46O7A)
  * using probabilistic neural network instead of CNN, methods seem old and the accuracy doesn't seem realistic
  
