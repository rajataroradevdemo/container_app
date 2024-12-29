import http from "../http-common";

const API_URL =  process.env.REACT_APP_API_URL;
const serverUrl = "http://" + API_URL + ":5000";


class TutorialDataService {
  getAll() {
    console.log("Calling getAllTutorial() Method from API")
    console.log("API_URL")
    console.log(API_URL)
    console.log("API URL Printed")
    return http.get(serverUrl + "/tutorials");
  }

  get(id) {
    return http.get(serverUrl + `/tutorials/${id}`);
  }

  create(data) {
    return http.post(serverUrl + '/tutorials', data);
  }

  update(id, data) {
    return http.put(serverUrl + `/tutorials/${id}`, data);
  }

  delete(id) {
    return http.delete(serverUrl + `/tutorials/${id}`);
  }

  deleteAll() {
    return http.delete(serverUrl + `/tutorials`);
  }

  findByTitle(title) {
    return http.get(serverUrl + `/tutorials?title=${title}`);
  }
}

export default new TutorialDataService();