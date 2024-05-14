from const import PATH_LOCATION_SOURCE, PATH_LOCATION_TARGET, PATH_TYPE_FOLDER, PATH_TYPE_FILE
from config import TAG_DATE_BEGIN, TAG_TARCK_END, TAG_OPTION_WHIP, TAG_OPTION_MOVE_SOURCE_TO_TARGET, TAG_OPTION_MOVE_TARGET_TO_SOURCE, TAG_OPTION_MPD_UPDATE
from session import S_CURRENT_SOURCE_FOLDER, S_CURRENT_TARGET_FOLDER, S_CURRENT_SOURCE_FOLDER_DISPLAY, S_CURRENT_TARGET_FOLDER_DISPLAY, S_CURRENT_TAG_ITEM
import streamlit as st
from api import list_folder_and_file_by_path, file_read_taginfo_by_path, file_write_taginfo_by_path
from datetime import datetime 
import uuid

# Session -------------------
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
    menu_items={
        'About': """
# Filemover for Home
살다가보면 가끔씩 MP3 Tag를 관리해야 할 일이 생기기 마련이다.

---

GitHub: [halfenif/test_streamlit_fastapi](https://github.com/halfenif/toy_filemover_streamlit)

Blog: [Enif's small talk](https://blog.enif.page/blog/)

---

"""
    }
)

# Title
st.title('Filemover for Home')

# Colums
c_source, c_target = st.columns(2, gap="small")

def fn_tag_info_submit():

    # st.error("이것은 에러 알림입니다.")
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

#@st.experimental_dialog("File Info")
def fn_file_info(fileitem):

    #Get Tag
    status_code, result = file_read_taginfo_by_path(fileitem)
    
    if status_code == 200:
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
                st.number_input(f"Year({TAG_DATE_BEGIN}~{year_end})", key="tagItem_tagDate", min_value=TAG_DATE_BEGIN, max_value=year_end, value=int(result["tagDate"]), step=1)
            else:
                st.number_input(f"Year({TAG_DATE_BEGIN}~{year_end})", key="tagItem_tagDate", min_value=TAG_DATE_BEGIN, max_value=year_end, value=TAG_DATE_BEGIN, step=1)

            if result["tagTracknumber"].isnumeric():
                st.number_input("Tracknumber(1~20)", key="tagItem_tagTracknumber", min_value=1, max_value=TAG_TARCK_END, value=int(result["tagTracknumber"]), step=1)
            else:
                st.number_input("Tracknumber(1~20)", key="tagItem_tagTracknumber", min_value=1, max_value=TAG_TARCK_END, value=1, step=1)

            # Options-Whip
            st.checkbox("Tag Whip(All tag clear before write)", key="tagItem_doWhip", value=TAG_OPTION_WHIP)
            
            # Options-Move To File
            if result["rootType"] == PATH_LOCATION_SOURCE:
                st.checkbox(f"Move to : Target > {st.session_state[S_CURRENT_TARGET_FOLDER_DISPLAY]}", key="tagItem_doMove", value=TAG_OPTION_MOVE_SOURCE_TO_TARGET)
            elif result["rootType"] == PATH_LOCATION_TARGET:
                st.checkbox(f"Move to : Source > {st.session_state[S_CURRENT_SOURCE_FOLDER_DISPLAY]}", key="tagItem_doMove", value=TAG_OPTION_MOVE_TARGET_TO_SOURCE)

            # Options-MPD
            st.checkbox("MPD Update", key="tagItem_doMpdUpdate", value=TAG_OPTION_MPD_UPDATE)

            # Set Button
            st.form_submit_button(label='Submit', on_click=fn_tag_info_submit)


        

#@st.experimental_dialog("Folder Info")
def fn_folder_info(fileitem):

    if fileitem["rootType"] == PATH_LOCATION_SOURCE:
        st.session_state[S_CURRENT_SOURCE_FOLDER] = fileitem["pathEncode"]
        st.session_state[S_CURRENT_SOURCE_FOLDER_DISPLAY] = fileitem["folderCurrent"]
    if fileitem["rootType"] == PATH_LOCATION_TARGET:
        st.session_state[S_CURRENT_TARGET_FOLDER] = fileitem["pathEncode"]
        st.session_state[S_CURRENT_TARGET_FOLDER_DISPLAY] = fileitem["folderCurrent"]

def fn_make_button_lable(fileitem):

    buttonEmoji = ""
    if fileitem["pathType"] == PATH_TYPE_FOLDER:
        buttonEmoji = ":file_folder:"
    if fileitem["pathType"] == PATH_TYPE_FILE:
        buttonEmoji = ":musical_note:"
    if fileitem["isParent"]:
        buttonEmoji = ":back:"
    
    return buttonEmoji + " " + fileitem["fileName"]

def fn_make_button_callback(fileitem):
    if fileitem["pathType"] == PATH_TYPE_FILE:
        return fn_file_info
    else:
        return fn_folder_info
    
    

#---------------------------------------------------------------------

# Container Source
with c_source:
    # Display
    st.subheader(f"Source >{str(st.session_state[S_CURRENT_SOURCE_FOLDER_DISPLAY])}")

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
    st.subheader(f"Target >{str(st.session_state[S_CURRENT_TARGET_FOLDER_DISPLAY])}")
    status_code, result = list_folder_and_file_by_path(PATH_LOCATION_TARGET, str(st.session_state[S_CURRENT_TARGET_FOLDER]))

    # debug
    # st.write(result)

    if status_code == 200:
        
        for fileitem in result:
            button_label = fn_make_button_lable(fileitem)
            button_callback = fn_make_button_callback(fileitem)            
            st.button(button_label, on_click=button_callback, args=[fileitem], key=uuid.uuid4())
