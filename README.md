<h1 align="center">
  <a href="" style="color:#9C276A">
    VLSA: Vision-Language-Action Models with<br>
    Plug-and-Play Safety Constraint Layer
  </a>
</h1>
<h5 align="center"> If our project helps you, please give us a star ⭐ on GitHub to support us. 🙏🙏 </h2>
<h5 align="center">

[![arXiv](https://img.shields.io/badge/Arxiv-2511.11891-AD1C18.svg?logo=arXiv)](https://arxiv.org/pdf/2512.11891) 
[![Website](https://img.shields.io/badge/Website-Project_Page-blue.svg?logo=googlechrome&logoColor=white)](https://vlsa-aegis.github.io/)
</h5> 

## 📢 Updates

- **[Dec 2025]** 📅 We plan to release the **SafeLIBERO benchmark** on **December 20**.
- **[Dec 9, 2025]** 🔥 Initial release of the **vlsa-aegis** repository.

 
## 📊 SafeLIBERO Benchmark
<p align="center">
  <img src="https://github.com/songqiaohu/pictureandgif/blob/main/safelibero_overview.png?raw=true" alt="overview" width="600">
</p>  

**SafeLIBERO** is a benchmark desinged to evaluate model performance in complex environments. It extends each LIBERO suite by selecting **four representative tasks**, with each task further divided into two scenarios with different safety levels, determined by the degree of interference introduced by an added obstacle: **Level I**: Scenarios where the obstacle is positioned in close proximity to the target object; **Level II**: Scenarios where the obstacle is located further away but obstructs the movement. It is worth noting that for some tasks, the distinction between these two intervention levels may be less obvious. Within each scenario, the positions of obstacles and other objects are randomized within a small range over 50 episodes to ensure robustness and diversity. A diverse set of everyday objects is used as obstacles, including **moka pots**, **storage boxes**, **milk cartons**, **wine bottles**, **mugs**, and **books**. Overall, SafeLIBERO consists of **4 suites comprising 16 tasks and 32 scenarios**, resulting in a total of **1,600 evaluation episodes**.

---

### 📚 Contents
- [Overview](#overview)
- [Benchmark Tasks](#benchmark-tasks)
- [Safety Constraints](#safety-constraints)
- [Evaluation Metrics](#evaluation-metrics)
- [Installation](#installation)
- [Getting Started](#getting-started)

---
