# Load .env
from env import Settings
config = Settings()

from const import PATH_LOCATION_SOURCE, PATH_LOCATION_TARGET, PATH_TYPE_FOLDER, PATH_TYPE_FILE

from session import S_CURRENT_SOURCE_FOLDER, S_CURRENT_TARGET_FOLDER # rerun() 했을 때 화면 갱신용
from session import S_CURRENT_SOURCE_FOLDER_DISPLAY, S_CURRENT_TARGET_FOLDER_DISPLAY # rerun() 했을 때 화면 갱신용
from session import S_CURRENT_TAG_ITEM # Tag Sidebar > API Server용
from session import S_CURRENT_FILE_ITEM # List > Tag Sidebar용
from session import S_CURRENT_ROOT_TYPE # 상단의 Header Folder용
from session import S_SB_STATE, S_SB_TAG_SELECT, S_SB_FOLDER_SELECT # Modal대신 Sidebar를 사용하긿 함

import streamlit as st
from api import list_folder_and_file_by_path, file_read_taginfo_by_path, file_write_taginfo_by_path
from datetime import datetime 
import uuid


# Session -------------------
if S_SB_STATE not in st.session_state:
    st.session_state[S_SB_STATE] = "collapsed"
if S_SB_TAG_SELECT not in st.session_state:
    st.session_state[S_SB_TAG_SELECT] = False
if S_SB_FOLDER_SELECT not in st.session_state:
    st.session_state[S_SB_FOLDER_SELECT] = False

if S_CURRENT_SOURCE_FOLDER not in st.session_state:
    st.session_state[S_CURRENT_SOURCE_FOLDER] = ''
    st.session_state[S_CURRENT_SOURCE_FOLDER_DISPLAY] = ''
if S_CURRENT_TARGET_FOLDER not in st.session_state:
    st.session_state[S_CURRENT_TARGET_FOLDER] = ''
    st.session_state[S_CURRENT_TARGET_FOLDER_DISPLAY] = ''

# Page Setup
st.set_page_config(
    page_title="Filemover for Home",
    page_icon=":musical_note:",
    initial_sidebar_state=st.session_state[S_SB_STATE],
    menu_items={
        'About': """
# Filemover for Home
살다가보면 가끔씩 MP3 Tag를 관리해야 할 일이 생기기 마련이다.

---

GitHub: [halfenif/toy_filemover_streamlit](https://github.com/halfenif/toy_filemover_streamlit)

Blog: [Enif's small talk](https://blog.enif.page/blog/)

---

[YoutubeDL-Material](https://github.com/Tzahi12345/YoutubeDL-Material) : Material Design frontend for youtube-dl.  
[MPD](https://www.musicpd.org/) : Music Player Daemon.  
[Home Assistant](https://www.home-assistant.io/) : My favorite Home Automation platform.  

---

"""
    }
)

# Sidebar Width
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 400px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)

#---------------------------------------------------------------------
# Function

def fn_file_select(fileitem):
    st.session_state[S_SB_TAG_SELECT]=True
    st.session_state[S_CURRENT_FILE_ITEM] = fileitem
    st.session_state[S_SB_STATE] = "expanded"

if st.session_state[S_SB_TAG_SELECT]:
    st.title(config.UI_OPTION_TITLE)
    #Reload Button for not submit escape
    button_reload = st.button(":arrows_counterclockwise: Reload")
    if button_reload:
        st.session_state[S_SB_TAG_SELECT] = False
        st.session_state[S_SB_STATE] = "collapsed"        
        st.rerun()

    fileitem = st.session_state[S_CURRENT_FILE_ITEM]

    #Get Tag
    status_code, result = file_read_taginfo_by_path(fileitem)
    
    if status_code == 200:
        with st.sidebar:
            with st.form("fileInfoForm"):

                # Set Serssion
                st.session_state[S_CURRENT_TAG_ITEM] = result

                # Set Form
                st.subheader(result["fileName"])
                st.text_input("File Base Name", result["fileBaseName"], key="tagItem_fileBaseName", max_chars=200)
                st.text_input("File Ext Name", result["fileExtName"], key="tagItem_fileExtName", max_chars=10, disabled=True)
                st.text_input("Title", result["tagTitle"], key="tagItem_tagTitle", max_chars=200)
                st.text_input("Album", result["tagAlbum"], key="tagItem_tagAlbum", max_chars=200)
                st.text_input("Artist", result["tagArtist"], key="tagItem_tagArtist", max_chars=200)
                st.text_input("Albumartist", result["tagAlbumartist"], key="tagItem_tagAlbumartist", max_chars=200)

                year_end = datetime.now().year
                if result["tagDate"].isnumeric():
                    st.number_input(f"Year({config.TAG_DATE_BEGIN}~{year_end})", key="tagItem_tagDate", min_value=config.TAG_DATE_BEGIN, max_value=year_end, value=int(result["tagDate"]), step=1)
                else:
                    st.number_input(f"Year({config.TAG_DATE_BEGIN}~{year_end})", key="tagItem_tagDate", min_value=config.TAG_DATE_BEGIN, max_value=year_end, value=config.TAG_DATE_BEGIN, step=1)

                if result["tagTracknumber"].isnumeric():
                    st.number_input("Tracknumber(1~20)", key="tagItem_tagTracknumber", min_value=1, max_value=config.TAG_TARCK_END, value=int(result["tagTracknumber"]), step=1)
                else:
                    st.number_input("Tracknumber(1~20)", key="tagItem_tagTracknumber", min_value=1, max_value=config.TAG_TARCK_END, value=1, step=1)

                # Options-Whip
                st.checkbox("Whip Tag :wastebasket: + :writing_hand:", key="tagItem_doWhip", value=config.TAG_OPTION_WHIP)
                
                # Options-Move To File
                if result["rootType"] == PATH_LOCATION_SOURCE:
                    st.checkbox(f"Move to :file_folder: :blue[Target > {st.session_state[S_CURRENT_TARGET_FOLDER_DISPLAY]}]", key="tagItem_doMove", value=config.TAG_OPTION_MOVE_SOURCE_TO_TARGET)
                elif result["rootType"] == PATH_LOCATION_TARGET:
                    st.checkbox(f"Move to :file_folder: :blue[Source > {st.session_state[S_CURRENT_SOURCE_FOLDER_DISPLAY]}]", key="tagItem_doMove", value=config.TAG_OPTION_MOVE_TARGET_TO_SOURCE)

                # Options-MPD
                st.checkbox("MPD Update :satellite_antenna: :loud_sound:", key="tagItem_doMpdUpdate", value=config.TAG_OPTION_MPD_UPDATE)

                # Set Button
                form_submited = st.form_submit_button(label='Submit')
                if form_submited:

                    tagItem = st.session_state[S_CURRENT_TAG_ITEM]

                    tagItem['fileBaseName'] = st.session_state['tagItem_fileBaseName']
                    tagItem['fileExtName'] = st.session_state['tagItem_fileExtName']
                    tagItem['tagTitle'] = st.session_state['tagItem_tagTitle']
                    tagItem['tagAlbum'] = st.session_state['tagItem_tagAlbum']
                    tagItem['tagArtist'] = st.session_state['tagItem_tagArtist']
                    tagItem['tagAlbumartist'] = st.session_state['tagItem_tagAlbumartist']
                    tagItem['tagDate'] = st.session_state['tagItem_tagDate']
                    tagItem['tagTracknumber'] = st.session_state['tagItem_tagTracknumber']

                    tagItem['doWhip'] = st.session_state['tagItem_doWhip']
                    tagItem['doMove'] = st.session_state['tagItem_doMove']
                    tagItem['doMpdUpdate'] = st.session_state['tagItem_doMpdUpdate']

                    if tagItem['rootType'] == PATH_LOCATION_SOURCE:
                        tagItem['pathToMoveEncode'] = st.session_state[S_CURRENT_TARGET_FOLDER]
                    elif tagItem['rootType'] == PATH_LOCATION_TARGET:
                        tagItem['pathToMoveEncode'] = st.session_state[S_CURRENT_SOURCE_FOLDER]

                    #Set Tag
                    file_write_taginfo_by_path(tagItem)

                    st.session_state[S_SB_TAG_SELECT] = False
                    st.session_state[S_SB_STATE] = "collapsed"
                    st.rerun()                    


        # End Modal Logic. Stop
        st.stop()
        

#---------------------------------------------------------------------
def fn_folder_select(fileitem):
    # Body Folder Select
    if fileitem["rootType"] == PATH_LOCATION_SOURCE:
        st.session_state[S_CURRENT_SOURCE_FOLDER] = fileitem["pathEncode"]
        st.session_state[S_CURRENT_SOURCE_FOLDER_DISPLAY] = fileitem["folderCurrent"]
    if fileitem["rootType"] == PATH_LOCATION_TARGET:
        st.session_state[S_CURRENT_TARGET_FOLDER] = fileitem["pathEncode"]
        st.session_state[S_CURRENT_TARGET_FOLDER_DISPLAY] = fileitem["folderCurrent"]

#---------------------------------------------------------------------
def fn_make_button_lable(fileitem):

    buttonEmoji = ""
    if fileitem["pathType"] == PATH_TYPE_FOLDER:
        buttonEmoji = ":file_folder:"
    if fileitem["pathType"] == PATH_TYPE_FILE:
        buttonEmoji = ":musical_note:"
    if fileitem["isParent"]:
        buttonEmoji = ":back:"

    display_file_name = buttonEmoji + " " + fileitem["fileNameDisplay"]
        
    return display_file_name

#---------------------------------------------------------------------
def fn_make_button_callback(fileitem):
    if fileitem["pathType"] == PATH_TYPE_FILE:
        return fn_file_select
    else:
        return fn_folder_select
    
#---------------------------------------------------------------------    
def fn_header_folder_select(rootType):
    # Header Folder Select
    st.session_state[S_SB_FOLDER_SELECT]=True
    st.session_state[S_CURRENT_ROOT_TYPE] = rootType
    st.session_state[S_SB_STATE] = "expanded"    

if st.session_state[S_SB_FOLDER_SELECT]:
    st.title(config.UI_OPTION_TITLE)
    #Reload Button for not submit escape
    button_reload = st.button(":arrows_counterclockwise: Reload")
    if button_reload:
        st.session_state[S_SB_FOLDER_SELECT] = False
        st.session_state[S_SB_STATE] = "collapsed"        
        st.rerun()

    with st.sidebar:
        with st.form("folderInfoForm"):
        
            st.subheader("Folder관련 기능 구현 예정")
            # Set Button
            form_submited = st.form_submit_button(label='Submit')
            if form_submited:
                st.session_state[S_SB_FOLDER_SELECT] = False
                st.session_state[S_SB_STATE] = "collapsed"
                st.rerun()  

        st.stop()

#---------------------------------------------------------------------
# Title
st.title(config.UI_OPTION_TITLE)

# Colums
c_source, c_target = st.columns(2, gap="small")


# Container Source
with c_source:
    # Display
    #st.subheader(f"Source >{str(st.session_state[S_CURRENT_SOURCE_FOLDER_DISPLAY])}")
    c_source.divider()
    st.button(f":card_file_box: Source >{str(st.session_state[S_CURRENT_SOURCE_FOLDER_DISPLAY])}", 
              on_click=fn_header_folder_select,
              args=[PATH_LOCATION_SOURCE],
              key=uuid.uuid4())

    

    # Read File List
    status_code, result = list_folder_and_file_by_path(PATH_LOCATION_SOURCE, str(st.session_state[S_CURRENT_SOURCE_FOLDER]))

    # debug
    # st.write(result)

    if status_code == 200:

        for fileitem in result:
            button_label = fn_make_button_lable(fileitem)
            button_callback = fn_make_button_callback(fileitem)
            st.button(button_label, on_click=button_callback, args=[fileitem], key=uuid.uuid4())


# Container Target
with c_target:
    # st.subheader(f"Target >{str(st.session_state[S_CURRENT_TARGET_FOLDER_DISPLAY])}")
    c_target.divider()    
    st.button(f":card_file_box: Target >{str(st.session_state[S_CURRENT_TARGET_FOLDER_DISPLAY])}",
              on_click=fn_header_folder_select,
              args=[PATH_LOCATION_TARGET],
              key=uuid.uuid4())
    

    status_code, result = list_folder_and_file_by_path(PATH_LOCATION_TARGET, str(st.session_state[S_CURRENT_TARGET_FOLDER]))

    # debug
    # st.write(result)

    if status_code == 200:
        
        for fileitem in result:
            button_label = fn_make_button_lable(fileitem)
            button_callback = fn_make_button_callback(fileitem)            
            st.button(button_label, on_click=button_callback, args=[fileitem], key=uuid.uuid4())
