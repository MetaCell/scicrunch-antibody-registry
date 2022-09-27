import { Antibody } from "../rest";
import { addAntibody } from "../services/AntibodiesService";

export function getProperCitation(a: Antibody) {
  return `(${a.vendorName}#${a.catalogNum}, RRID:AB_${a.abId})`;
}

export function postNewAntibody(a: Antibody, props) {
  addAntibody(a)
    .then((res) => {
      props.setAntibodyId(res.abId);
      props.setApiResponse({ status: 200, detail: res.abId });
      props.next();
    })
    .catch((err) => {
      const { status, data } = err.response;
      if (status === 409) {
        let id = data.detail.split(" ")[7].match(/\d/g).join("");
        props.setApiResponse({
          status: 409,
          detail: data.detail,
        });
        props.setAntibodyId(id);
      } else {
        props.setApiResponse({
          status,
          detail: data.detail,
        });
      }
      props.next();
    });
}
