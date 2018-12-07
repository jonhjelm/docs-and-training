from clfpy import HpcImagesClient
from clfpy import GssClient
from clfpy import AuthClient

auth = AuthClient("https://api.hetcomp.org/authManager/AuthManager?wsdl")
user = "???"
project = "???"
password = "???"

print("Authenticating ...")
tk = auth.get_session_token(user, project, password)

print("Uploading image ...")
gss = GssClient("https://api.hetcomp.org/gss-0.1/FileUtilities?wsdl")
gss_ID = "it4i_anselm://home/abortable_waiter.simg"
# Change to gss.upload for the first upload
gss.update(gss_ID, tk, "abortable_waiter.simg")

print("Registering image ...")
images = HpcImagesClient("https://api.hetcomp.org/hpc-4-anselm/Images?wsdl")
# Change to images.upload_image for the first upload
images.update_image(tk, "waiter_abortable.simg", gss_ID)

print("Querying image information ...")
print(images.get_image_info(tk, "waiter_abortable.simg"))
