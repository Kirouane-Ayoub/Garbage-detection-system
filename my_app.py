import streamlit as st 
import os 
from PIL import Image
from str_object_detect import detect
from ob_detect import run
import time 
st.sidebar.image("icon.png")
model_type = st.sidebar.selectbox("Detect FROM : " , ["Drone" , "CCTV"])
if model_type == "Drone" : 
    model_path = "rubbish_drones.pt"
else : 
    model_path = "garbage_cctv3.pt"
select_type_detect = st.sidebar.selectbox("Detection from :  ",
                                          ("File", "Live"))
select_device = st.sidebar.selectbox("Select compute Device :  ",
                                       ("CPU", "GPU"))
if select_device == "GPU" : 
    DEVICE_NAME = st.selectbox("Select CUDA index : " , 
                                      (0, 1 , 2)) 
elif select_device =="CPU" : 
    DEVICE_NAME = "cpu"

save_output_video = st.sidebar.radio("Save output video?",('Yes', 'No'))
if save_output_video == 'Yes':
    nosave = False
    display_labels=True
else:
    nosave = True
    display_labels = True
conf_thres = st.sidebar.text_input("Class confidence threshold", "0.25")

def fromvid(source, conf_thres , device , vid_id , nosave  , display_labels) :
    kpi5, kpi6 = st.columns(2)
    with kpi5:
        st.markdown("""<h5 style="color:white;">
                                  CPU Utilization</h5>""", 
                                  unsafe_allow_html=True)
        kpi5_text = st.markdown("0")
    with kpi6:
        st.markdown("""<h5 style="color:white;">
                                Memory Usage</h5>""", 
                                unsafe_allow_html=True)
        kpi6_text = st.markdown("0")
    stframe = st.empty()
    detect(weights=model_path,
                   source=source,
                   stframe=stframe, 
                   kpi5_text=kpi5_text , 
                   kpi6_text=kpi6_text, 
                   conf_thres=float(conf_thres),
                   device=device,
                   hide_labels=False,  
                   hide_conf=False,
                   project=vid_id, 
                   nosave=nosave, 
                   display_labels=display_labels)

if select_type_detect == "File" :
    tab0 , tab1, tab2 = st.tabs([ "Home", 
                                  "Image",
                                  "Video"])
    with tab0 :
        st.header("About UAVVaste Dataset : ")
        st.image("garb.png")
        st.write("The UAVVaste dataset consists to date of 772 images and 3716 annotations. The main motivation for creation of the dataset was the lack of domain-specific data. The datasets that are widely used for object detection evaluation benchmarking. The dataset is made publicly available and is intended to be expanded.")
        st.write("for more information about it, you can visit the official website from here  : ")
        st.write("https://uavvaste.github.io/")
        st.image("uavvaste_example.gif")
         
        st.header("About This Project : ")
        st.write("""The Illegal Garbage Detection System is a high-tech solution that uses drones or CCTV cameras equipped with the YOLOv5 algorithm to detect and alert individuals of illegal garbage dumping in the surrounding area. 
        The system is designed to work in real-time, constantly monitoring the environment and providing accurate and timely notifications of any illegal garbage detected. 
        The use of drones allows for a wider coverage area and the ability to access hard-to-reach areas while CCTV cameras are utilized to monitor specific areas where illegal dumping is known to occur. The YOLOv5 algorithm is a powerful machine learning tool that is able to detect and classify objects in real-time, 
        making it a valuable tool in detecting illegal garbage and helping to keep the environment clean.
""")
    with tab1:
        image_id = str(time.asctime())
        st.header("Image")
        image_upload = st.file_uploader("upload your image" , 
                                        type=["png" , "jpg"])
        try : 
            run(weights=model_path, 
            source=image_upload.name, 
            device=DEVICE_NAME ,
            name=image_id)
            image = Image.open(f"{image_id}/{image_upload.name}")
            st.image(image)
        except : 
            pass
    
    with tab2 :
        vid_id = str(time.asctime())
        st.header("Video")
        video_upload = st.file_uploader("upload your Video" , 
                                        type=['mp4', 'mov'])
        if video_upload : 
            if st.button('Click to start'):
                fromvid(source=video_upload.name ,  
                        vid_id=vid_id , 
                        device=DEVICE_NAME , 
                        conf_thres=conf_thres ,
                        nosave=nosave ,
                        display_labels=display_labels)
                
                

elif select_type_detect == "Live" : 
    live_id = str(time.asctime())
    live_type = st.selectbox("Live Type :  ",
                             ("URL", "WEBCAM"))
    if live_type=="URL":
        url = st.text_input('Entre your URL stream : ')
        if url : 
            fromvid(source=url ,
             vid_id=live_id , 
             device=DEVICE_NAME , 
             conf_thres=conf_thres ,
             nosave=nosave , 
             display_labels=display_labels )
    elif live_type=="WEBCAM" : 
        cam_id = str(time.asctime())
        index = st.selectbox("Select Device index : " , 
                              (0, 1 , 2))
        if st.button('Run Detection'):           
            os.system(f"python objectDetect_tracking.py --source {index} --view-img --conf-thres {conf_thres} --device {DEVICE_NAME} --project '{cam_id}' --color-box")
