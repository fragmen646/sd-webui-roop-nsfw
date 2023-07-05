import os
import pkg_resources
import sys
from tqdm import tqdm
import urllib.request

req_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "requirements.txt")

models_dir = os.path.abspath("models/roop")
model_url = "https://huggingface.co/henryruhs/roop/resolve/main/inswapper_128.onnx"
model_name = os.path.basename(model_url)
model_path = os.path.join(models_dir, model_name)

def download(url, path):
    request = urllib.request.urlopen(url)
    total = int(request.headers.get('Content-Length', 0))
    with tqdm(total=total, desc='Downloading', unit='B', unit_scale=True, unit_divisor=1024) as progress:
        urllib.request.urlretrieve(url, path, reporthook=lambda count, block_size, total_size: progress.update(block_size))

if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(model_path):
    download(model_url, model_path)

with open(req_file) as file:
    for package in file:
        try:
            package = package.strip()

            if "==" in package:
                package_name, package_version = package.split('==')
                try:
                    installed_version = pkg_resources.get_distribution(package_name).version
                    if installed_version != package_version:
                        print(
                            f"Running install of {package}, {installed_version} vs {package_version}"
                        )
                        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                except pkg_resources.DistributionNotFound:
                    print(f"Installing {package} as it is not found.")
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            else:
                try:
                    pkg_resources.get_distribution(package)
                except pkg_resources.DistributionNotFound:
                    print(f"Installing {package} as it is not found.")
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

        except Exception as e:
            print(e)
            print(f"Warning: Failed to install {package}, nsfw-roop will not work.")
            raise e
