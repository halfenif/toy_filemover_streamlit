# Filemover for Home (MP3 Tag Manager)

![Demo](https://github.com/halfenif/toy_filemover_streamlit/tree/main/doc/Screen01.png)

## Demo
[https://filemover.enif.page](https://filemover.enif.page)

## Installation
**Requirements**
- Docker, Docker-Compose or Podman

### Clone
```bash
git clone https://github.com/halfenif/toy_filemover_streamlit.git
```

### Set MP3 Folder
Default folder path **'/mnt/folder_source'** & **'/mnt/folder_target'**   
change docker-compose.yml file

## Change Config (Options)
```bash
cp ./fastapi/.env.sample ./fastapi/.env
cp ./streamlit/.env.sample ./streamlit/.env
```
**fastapi/.env**
- ENV_TYPE = ".env.sample" > ".env" Display Information
- IS_DEBUG = bool
- MPD_SERVER_IP, MPD_SERVER_PORT = if you use MPD
- UI_OPTION_SHORT_FILE_NAME = bool. Display button label short or not
- UI_OPTION_SHORT_FILE_LENGTH = int. Display button label char count
- FILE_OPTION_UPLOAD_LIMIT_MB = int. Use .env insted of streamlit/.streamlit/config.toml

**streamlit/.env**
- ENV_TYPE = ".env.sample" > ".env" Display Information
- URL_BACKEND = fastAPI container URL
- UI_OPTION_TITLE = str, st.title(), if "" is None
- UI_OPTION_DESC = str, st.write(), if "" is None
- UI_OPTION_SIDEBAR_WIDTH = int, st.sidebar width
- TAG_DATE_BEGIN, TAG_TARCK_END = int tag default value
- TAG_OPTION_WHIP = bool. Check Box Defualt Value
- TAG_OPTION_MOVE_SOURCE_TO_TARGET, TAG_OPTION_MOVE_TARGET_TO_SOURCE = bool. Check Box Defualt Value
- TAG_OPTION_MPD_UPDATE = bool. Check Box Defualt Value


### Docker-Compose
```bash
docker-compose build
docker-compose up
```

### Podman
```bash
./rebuild_podman.sh
```

---
### Below Korean Description
## 이 녀석을 만들게된 이야기

요즘 세상에 누가 MP3로 음악을 듣겠습니까 마는, 저는 1년에 한 두번 MP3 Tag를 수정 할 일이 생기는 삶을 살고 있습니다.

아주 오래전부터 [MPD](https://www.musicpd.org/)를 사용해서 음악환경을 구축하고 있었기 때문에 음악파일(대부분 MP3)은 NAS의 특정 폴더에 저장되어있고, 다양한 MPD가 cifs로 접근하고 있는 상황입니다.

거의 그럴일은 없지만, 일년에 몇 개의 MP3 File이 신규로 유입(Source Folder)되는 상황이 발생하고, 불행히도 그 파일들은 MPD의 Music Folder(Target Folder)와는 상이한 상황이다 보니.

어디선가 굴러다니고 있을 GUI Tag Editor를 찾아서 Tag를 바꾸고, NAS의 Music Folder에 Copy하고, MPC update명령을 (집사람에게 알려준다고 가능할리가...) 실행하는게 귀찬아서 만들게되었습니다.

이 녀석을 [Home Assistant](https://www.home-assistant.io/) lovelace에 설정하고 친절(?)하게 알려준다면, 사용자가 스스로 MP3 Tag를 정리 할 수 있지 않을까요? (누구나 희망을 가지고 있다. 아마도.)

### 생각해볼만한 기술적 사항들
- streamlit은 진정 간편하게 UI(Front)를 구성할 수 있지만. 그것이 가지는 설계사상에 순응하며 구현 할 생각을 해야 속편하다 생각됩니다.
- File upload, delete, Folder Add, Rename, Delete, Move가 필요하다고 생각하지만. File은 고민좀 해보고, Folder는 적절한 UI가 생각나지 않습니다.
- logging은 구현하면서보니 아직까지 필요하지는 않았습니다.
- Exception처리는 화면에 표출하는게 좋겠다 싶어 Result Class를 반환하는 방식을 사용합니다.
- 파일경로를 Base64로 인코딩하는 이유는 (습관적인 것이니 괘념치 마시지 바랍니다.)

---
아직은 알파버전이이지만, 사용자 테스트를 진행하고 (필요하다면)업데이트 하도록 하겠습니다.
2024.05.14. By HalfEnif