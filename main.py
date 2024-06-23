from fastapi import FastAPI, UploadFile, File,HTTPException
from PIL import Image,UnidentifiedImageError
app = FastAPI()

@app.get("/details") #have to put my name and roll no as required parameters else it will show error 
def info(name:str,roll_no:int):
    try:
        name={"name":name,"roll no":roll_no}
        return(name)
    except Exception as e:
        raise HTTPException(status_code=404,details="some error occured while processing:{str(e)}")

@app.post("/resize")
async def resize_image(name:str,roll_no:int,passportphoto:UploadFile=File(),width:int=300,height:int=300):
    details={"name":name,"roll_no":roll_no,"message":"The resized image has been saved in the imgtool folder of this PC by a new name as newimage1.png"}
    try:
        img = Image.open(passportphoto.file) #Open the image using syntax "open" which fetch the image data through the uploaded file
    except UnidentifiedImageError:
        raise HTTPException(status_code=400,detail="please upload a vaild image")
    except Exception as e:
        raise HTTPException(status_code=401,details=f"some error occured while opening the file:{str(e)}")
    try:
        resized_image = img.resize((int(width),int(height))) #Resize the image to 300*300 ratio using the syntax "resize"
    except Exception as e:
        raise HTTPException(status_code=402,detail=f"some kind of error while resizing the image:{str(e)}")
    try:
        resized_image.save("newimage1.png")  #saves the image in my pc in imgtool folder
    except Exception as e:
        raise HTTPException(status_code=403,detail=f"some kind of error occured while saving the file in the directory,may possible that the directory dosnt exist:{str(e)}")
    return(details)  #returns the details which student has given and delivers a message alongwith
@app.post("/compression")
async def compress_image(quality: int = 20, uploadphoto: UploadFile = File()):
    try:
        compimage = Image.open(uploadphoto.file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Some error occurred while opening the image file: {str(e)}")
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Please upload a valid image")
    if(quality<1 or quality>95):
        raise HTTPException(status_code=400,detail="invalid value of quality selected please select between 1 and 95")
    try:
        # Save the compressed image with specified quality
        compimage.save("newcompimage2.png", optimize=True, quality=quality)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Some error occurred while saving the image, maybe the directory doesn't exist: {str(e)}")

    details = {"message": "The compressed file has been saved to the imgfolder with name newcompimage2.png"}
    return details