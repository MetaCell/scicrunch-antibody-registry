import { Antibody } from "../rest";
import { addAntibody } from "../services/AntibodiesService";

export function postNewAntibody(
  a: Antibody,
  setAntibodyId: (id: string) => void,
  setApiResponse: (obj: {}) => void,
  next: () => void
) {
  addAntibody(a)
    .then((res) => {
      setAntibodyId(res.abId);
      setApiResponse({ status: 200, detail: res.abId });
      next();
    })
    .catch((err) => {
      const { status, data } = err.response;
      if (status === 409) {
        setApiResponse({
          status: 409,
          detail: data.abId,
        });
        setAntibodyId(data.abId);
      } else {
        setApiResponse({
          status,
          detail: data.detail,
        });
      }
      next();
    });
}
