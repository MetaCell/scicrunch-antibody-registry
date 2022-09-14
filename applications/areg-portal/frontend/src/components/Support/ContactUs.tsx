import React from "react";

import SupportTabs from "../UI/SupportTabs";

const ContactUs = () => {
  let text = 'Hello\nAigul\nfiuheuh'
  return (
    <SupportTabs>
      <div style={{ "whiteSpace": "pre-wrap" }}>{text}</div>
    </SupportTabs>
  )
}

export default ContactUs;