export default function getUrlsByIds(ids, cameras) {
  let result = {};
  for (let i = 0; i < ids.length; i++) {
    let id = ids[i];
    if (id in cameras) {
      result[id] = cameras[id].url ;
    }
  }
  return result;
}