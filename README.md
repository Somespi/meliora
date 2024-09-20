<p align="center" width="100%">
<img src="./images/logo.svg" width="200">
<br><br>
meliora is a command-line tool for sorting files based on their content. that's it. 
<br>
<img src="./images/hero.svg" width="800">
</p>


## Requirements
Python 3.x

## Installation


1. Clone the repository:
```shell
git clone https://github.com/somespi/meliora.git
```

<details>
<summary>Installing using <code>meliora-setup</code></summary> 

2. Change into the project directory
```shell
cd meliora
```` 

3. run `meliora-setup.py` 
```shell
python meliora-setup.py
```
<br>
</details>

<details>
<summary>Installing Manually</summary> 


2. Change into the project directory (**Do it twice**, one to enter the project directory and the other for entring the src):

```shell
cd meliora
```




3. Install the required dependencies:
```shell
pip install -r requirements.txt
```

4. Download the en_core_web_md model for Spacy:

```shell
python -m spacy download en_core_web_md
```


5. Install meliora:

```shell 
cd ..
```

- If you want to install it globally:
```shell
pip install .
```

- If you want to install it locally for development purposes:
```shell
pip install -e .
```

6. run meliora: 
```shell
python -m meliora <DIRECTORY_PATH>
```

</details>
