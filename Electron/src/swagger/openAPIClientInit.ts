import Global from "global/global";
import { OpenAPI } from "./api/core/OpenAPI";

const initOpenAPIClient = () => {
    OpenAPI.WITH_CREDENTIALS = true;
    OpenAPI.BASE = Global.backendBaseUrl;
  };

export default initOpenAPIClient