podman container stop filemover_streamlit
podman container stop filemover_fastapi

podman container rm filemover_streamlit
podman container rm filemover_fastapi

podman-compose build
podman-compose up --detach
