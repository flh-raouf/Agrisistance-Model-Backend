import zipfile

def zip_model(model_file, zip_file):
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(model_file, arcname=model_file)

if __name__ == "__main__":
    model_file = 'crop_model.joblib'
    zip_file = 'crop_model.zip'
    zip_model(model_file, zip_file)
    print(f"Model compressed and saved as {zip_file}")
