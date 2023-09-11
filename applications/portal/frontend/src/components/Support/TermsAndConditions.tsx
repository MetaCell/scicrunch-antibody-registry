import React from "react";

import SupportTabs from "../UI/SupportTabs";
import { Container, Stack, Card, CardContent, Typography, Link } from "@mui/material";

const BasicCard=(props) => {
  return (
    <Card elevation={0} sx={{ backgroundColor:'grey.50' }}>
      <CardContent>

        <Typography variant="h5" component="div" sx={{ mb: 1.5, color:'grey.700', fontSize:'1.5rem' }} >
          {props.title}
        </Typography>

        <Typography variant="body2" sx={{ whiteSpace:'pre-line', color:'grey.700', fontSize:'1rem', textAlign:'left',  }}>
          {props.children}
        </Typography>
      </CardContent>
    </Card>
  );
}

const termsArray=[{
  title:'Terms of Use',
  content:`These Terms of Use are a contract between you and The Antibody Registry. The Antibody Registry operated website http://antibodyregistry.org, and products, services and affiliated websites offered by the The Antibody Registry; collectively The Antibody Registry "Sites/Services." Through these services the SciCrunch provides a dynamic inventory of Web-based neuroscience resources, data, and tools. The Antibody Registry advances neuroscience research by enabling discovery and access to public research data and tools worldwide through an open source, networked environment.\n
  By using the The Antibody Registry's Sites/Services, you are agreeing to be bound by the following terms and conditions ("Terms of Use"). If you do not agree to these Terms of Use, do not visit or use the The Antibody Registry's Sites/Servic`
},
{
  title:'Ownership of Content',
  content:`The copyright in the material contained in and provided by the The Antibody Registry's Sites/Services belongs to The Antibody Registry or its licensors. The trademarks and other elements appearing on the The Antibody Registry's Sites/Services are protected by California, United States, and international copyright, trade dress, patent, and trademark laws, international conventions and all other relevant intellectual property and proprietary rights and applicable laws. All content of the The Antibody Registry Sites/Services, except where otherwise noted, is licensed under a `,
  link: "Creative Commons Attribution License",
  url: "https://creativecommons.org/licenses/by/3.0/"
},
{
  title:'Reproduction of Data',
  content:`All data indexed and referenced by The Antibody Registry through the The Antibody Registry's Sites/Services, unless otherwise indicated, are licensed by the respective owners of such data. Use and distribution is subject to the Terms of Use by the original resource as well as citation of The Antibody Registry and the original source in accordance with the Creative Commons Attribution License.`
},{
  title:'Privacy',
  content:'You confirm that you have read and accept our',
  url:'https://scicrunch.org/page/privacy',
  link:'Privacy Policy'
},
{
  title:'General Practices Regarding Use',
  content:`The Antibody Registry reserves the right to limit, suspend or terminate your access and use of the The Antibody Registry's Sites/Services at any time without notice.`
},
{
  title:'Your Account(s)',
  content: 'In order to open an "Account" for use of certain Antibody Registry Sites/Services, you must (i) agree to these Terms of Use, (ii) agree to the ',
  content2:`and (iii) provide any information required by The Antibody Registry during the registration process. You are responsible for maintaining the accuracy of this information, and the security of your Account and password. The Antibody Registry cannot and will not be liable for any loss or damage from your failure to comply with this security obligation. You are also responsible for all content that you may post on the The Antibody Registry's Sites/Services and activity that occurs under your Account (even when content is posted by others under your Account). You shall: (i) notify The Antibody Registry immediately of any unauthorized use of any password or Account or any other known or suspected breach of security; and (ii) report to The Antibody Registry immediately and use reasonable efforts to stop immediately any unauthorized activity that is known or suspected by you.`,
  url:'https://creativecommons.org/licenses/by/3.0/',
  link:'Creative Commons Attribution License' 
},
{ title:'Impermissible Acts',
  content:`As a condition to your use of the The Antibody Registry Sites/Services, you agree not to:

`,
  content2:<>
<li>upload, post, email, transmit or otherwise make available any information, materials or other content that is illegal, harmful, threatening, abusive, harassing, defamatory, obscene, pornographic, or offensive; or that infringes another's rights, including any intellectual property rights;</li>
<li>impersonate any person or entity or falsely state or otherwise misrepresent your affiliation with a person or entity; or obtain, collect, store or modify personal information about other users;</li>
<li>upload, post, email, transmit or otherwise make available any unsolicited or unauthorized advertising, promotional materials, "junk mail," "spam," "chain letters," "pyramid schemes," or any other form of solicitation;</li>
<li>modify, adapt or hack the The Antibody Registry's Sites/Services or falsely imply that some other site or service is associated with The Antibody Registry's Sites/Services or The Antibody Registry's; or</li>
<li>use the The Antibody Registry's Sites/Services for any illegal or unauthorized purpose. You must not, in the use of The Antibody Registry's Sites/Services, violate any laws in your jurisdiction (including but not limited to copyright laws).</li></> },
{
  title:'Violation of these Terms of Use',
  content:`The Antibody Registry reserves the right to investigate and prosecute violations of any of these Terms of Use to the fullest extent of the law. The Antibody Registry may involve and cooperate with law enforcement authorities in prosecuting users who violate the Terms of Use. You acknowledge that The Antibody Registry has no obligation to pre-screen or monitor your access to or use of The Antibody Registry's Sites/Services or any information, materials or other content provided or made available through the The Antibody Registry's Sites/Services, but has the right to do so. You hereby agree that The Antibody Registry may, in the exercise of The Antibody Registry's sole discretion, remove or delete any entries, information, materials or other content that violates these Terms of Use or that is otherwise objectionable.`
},
{
  title:'Feedback',
  content:`In the course of using The Antibody Registry's Sites/Services, you may provide The Antibody Registry with feedback, including but not limited to suggestions, observations, errors, problems and defects regarding The Antibody Registry's Sites/Services (collectively "Feedback"). You hereby grant The Antibody Registry's a worldwide, irrevocable, perpetual, royalty-free, transferable and sub-licensable, non-exclusive right to use, copy, modify, distribute, display, perform, create derivative works from and otherwise exploit all such Feedback.`
},
{
  title:'Modifications to SciCrunch Sites/Services and Terms of Use',
  content:`The Antibody Registry reserves the right to modify or discontinue, temporarily or permanently, The Antibody Registry's Sites/Services (or any part thereof) with or without notice at any time. You agree that The Antibody Registry shall not be liable to you or to any third party for any modification, suspension or discontinuance of the The Antibody Registry's Sites/Services. The Antibody Registry reserves the right to change these Terms of Use by posting changes on this page of the The Antibody Registry's Sites. By using The Antibody Registry's Sites/Services, you agree to be bound by any such revisions and should therefore periodically visit this page to determine the then-current Terms of Use to which you are bound.`
},
{
  title:'Links',
  content:`The Antibody Registry's Sites/Services, or relevant third parties, may provide links to other web sites or resources. Because The Antibody Registry has no control over such sites and resources, you acknowledge and agree that The Antibody Registry is not responsible for the availability of such external sites or resources, and does not endorse and is not responsible or liable for any content, advertising, products or other materials on or available from such sites or resources. Your business dealings with any third-parties through the The Antibody Registry's Sites, including payment and delivery of related goods or services, and any other terms, conditions, warranties or representations associated with such dealings, are solely between you and such third party. You further acknowledge and agree that The Antibody Registry shall not be responsible or liable, directly or indirectly, for any damage or loss caused or alleged to be caused by or in connection with use of or reliance on any such content, goods or services available on or through any such site or resource.`
},
{ title:'Software/Technology in Use by The Antibody Registry',
  content:'The Antibody Registry codebase is in github: https://github.com/MetaCell/scicrunch-antibody-registry. Code License Apache 2.0' },
{ title:'Notification of Claims of Infringement',
  content:`If you believe that your work has been copied in a way that constitutes copyright infringement, or your intellectual property rights have otherwise been violated, please ${" "} `,
  url:'mailto:abr-help@scicrunch.org',
  link:'notify us' },
{
  title:'Disclaimer of Warranties',
  content:`YOUR USE OF The Antibody Registry's SITES, SERVICES OR ANY WEB SITE TO WHICH THEY ARE LINKED IS AT YOUR SOLE RISK. The Antibody Registry's SITES/SERVICES AND THEIR CONTENT ARE PROVIDED FOR USE ON AN "AS IS" AND "AS AVAILABLE" BASIS. The Antibody Registry MAKES NO REPRESENTATIONS OR WARRANTIES WITH RESPECT TO The Antibody Registry's SITES/SERVICES OR THEIR CONTENTS AND HEREBY DISCLAIMS ALL WARRANTIES, EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, OR NON-INFRINGEMENT RELATING TO The Antibody Registry's SITES/SERVICES, THEIR CONTENT OR ANY WEB SITE TO WHICH THEY ARE LINKED.

  NO ADVICE OR INFORMATION, WHETHER ORAL OR WRITTEN, OBTAINED BY YOU FROM The Antibody Registry OR THROUGH OR FROM THE SCICRUNCH SITES/SERVICES SHALL CREATE ANY WARRANTY NOT EXPRESSLY STATED IN THE TERMS OF USE. WITHOUT LIMITING THE GENERALITY OF THE FOREGOING, SCICRUNCH STRONGLY RECOMMENDS THAT YOU INDEPENDENTLY VERIFY ANY MEDICAL TREATMENT INFORMATION UPON WHICH YOU CHOOSE TO RELY.`
},{
  title:'Indemnification',
  content:`You agree to indemnify and hold The Antibody Registry, and its subsidiaries, affiliates, officers, agents, co-branders or other partners and employees, harmless from any claim or demand, including reasonable attorney fees, made by any third party due to or arising out of your use of the The Antibody Registry's Sites/Services, your connection to the The Antibody Registry's Sites/Services, your violation of these Terms of Use, your violation of any rights of another, or any breach of the foregoing representations, warranties and covenants. The user is solely responsible for his or her actions when using the The Antibody Registry's Sites/Services, including, but not limited to, costs incurred for Internet access. The Antibody Registry reserves the right, at our own expense, to assume the exclusive defense and control of any matter for which you are required to indemnify us, and you agree to cooperate with our defense of these claims. Limitation of Liability

  IN NO EVENT SHALL The Antibody Registry OR ITS EMPLOYEES, AGENTS, SUPPLIERS OR CONTRACTORS BE LIABLE FOR ANY DAMAGES OF ANY NATURE, INCLUDING WITHOUT LIMITATION ANY CONSEQUENTIAL LOSS, DAMAGES FOR LOSS OF INCOME OR PROFIT, LOSS OF OR DAMAGE TO PROPERTY, LOSS OF GOODWILL, USE, DATA OR OTHER INTANGIBLE LOSSES, CLAIMS OF THIRD PARTIES, OR ANY OTHER LOSS, COST, CLAIM OR EXPENSE OF ANY KIND OR CHARACTER ARISING OUT OF OR IN CONNECTION WITH THE USE OF THE The Antibody Registry's SITES/SERVICES, THEIR CONTENT OR ANY WEB SITE WITH WHICH THEY ARE LINKED.`

},
{
  title:'Special Considerations for International use',
  content:'Recognizing the global nature of the Internet, you agree to comply with all local rules regarding online conduct. Specifically, you agree to comply with all applicable laws regarding the transmission of technical data exported from the United States or the country in which you reside.'
},
{ title:'General Terms',
  content:`These Terms of Use constitute the entire agreement between you and The Antibody Registry and govern your use of the The Antibody Registry's Sites/Services, superseding any prior agreements between you and The Antibody Registry (including, but not limited to, any prior versions of the Terms of Use) and any prior representations by The Antibody Registry. These Terms of Use shall be governed by and construed in accordance with the laws of the State of California, without regard to conflicts of law principles. The failure of The Antibody Registry to exercise or enforce any right or provision of the Terms of Use shall not constitute a waiver of such right or provision. If any provision of the Terms of Use is found by a court of competent jurisdiction to be invalid, the parties nevertheless agree that the court should endeavor to give effect to the parties' intentions as reflected in the provision, and the other provisions of the Terms of Use remain in full force and effect. You agree that regardless of any statute or law to the contrary, any claim or cause of action brought against The Antibody Registry and its subsidiaries, affiliates, officers, agents, co-branders or other partners and employees, arising out of or related to use of the The Antibody Registry Sites/Services or the Terms of Use must be filed within one (1) year after such claim or cause of action arose or be forever barred. The section titles in the Terms of Use are for convenience only and have no legal or contractual effect.

The "Terms of Use" posted on this site was updated on or about March 10, 2017 (Version 1.0).

These "Terms of Use" were adapted from the PLoS Terms of Use which are licensed under a`,
  url:'http://creativecommons.org/licenses/by/2.5/',
  link:'Creative Commons Attribution License' },
{
  title:'The Antibody Registry Privacy Statement',
  content:`The Antibody Registry is dedicated to protecting personal information and will make every reasonable effort to handle collected information appropriately. All information collected, as well as related requests, will be handled as carefully and efficiently as possible. This Privacy Policy applies to all of the products, services and websites offered by The Antibody Registry; collectively, The Antibody Registry's "Site/Services."`
},
{
  title:'The collection of personal information',
  content:'In some circumstances, we may request personal information from you, like your name, e-mail address, institutional name, or telephone number. Your response to these inquiries is strictly voluntary. The Antibody Registry uses this information to customize your experience and interface with our electronic resources. In general, you can visit our site and utilize our services without divulging any personal information.'
},
{
  title:'Collecting domain information',
  content:`The Antibody Registry also collects domain information as part of its analysis of the use of this site. This data includes, but is not limited to, information about:

  `,
  content2:<>

    <li>Internet domain (for example, "yourschool.edu") and your computer's unique IP address;</li>
    <li>if you linked to a The Antibody Registry service indirectly from another Web site, the IP address of that Web site;</li>
    <li>type of browser software and operating system used to access The Antibody Registry's services;</li>
    <li>date and time of your visit;</li>
    <li>identity of pages you visit;</li>
 <br/>
  <span>This data enables us to become more familiar with which customers visit our site, how often they visit, and what parts of the site they visit most often. The Antibody Registry uses this information to improve its Web-based offerings and services. This information is collected automatically and requires no action on your part.</span>
  </>
},
{
  title:'Disclosure to third parties',
  content:'We treat your information as private and confidential, and we will not disclose your data to third parties without your express permission or unless required by law, or deemed necessary to protect and defend our rights or property or those of others. We do not collect information or create individual profiles with the information you provide for commercial marketing.'

},{
  title:'Use of cookies',
  content:`Some pages on this site may use "cookies," which are small files that the site places on your hard drive for identification purposes. These files are used for site registration and customization the next time you visit us. You should note that cookies cannot read data off of your hard drive. Your Web browser may allow you to be notified when you are receiving a cookie, giving you the choice to accept it or not. By not accepting cookies, some pages may not fully function and you may not be able to access certain information on this site.

  This statement may change from time to time, so please check back periodically. Each version of this Privacy Policy will be identified by its effective date. If you have any concerns about how your information is being used or questions about The Antibody Registry's Privacy Policy, please feel free to `,
  url:'https://www.scicrunch.com/contact',
  link:'contact us.',
  content2:<>
  <br/><br/>
  <span>The Privacy Statement posted on this site was updated on or about March 10, 2017, (Version 1.0).</span>
  <br/><br/>
  <span>This Privacy Policy was adapted from the PLoS Privacy Policy which is licensed under a <Link href='https://creativecommons.org/licenses/by/2.5/'>Creative Commons Attribution License</Link></span></>
}]

const TermsAndConditions = () => {
  const styles = {
    container:{ display:'flex', justifyContent:'center' }
  }
  
  return (
    <SupportTabs>
      <Container maxWidth='xl' sx={styles.container} className="container-terms-conditions">
        <Stack spacing={4}>
          <Typography variant='h1' color='grey.700'>Terms and Conditions</Typography>
          {termsArray.map((ele,index) => <BasicCard key={index}title={ele.title} >{ele.content}{ele.link && <Link href={ele.url}>{ele.link}</Link>}{ele.content2? ele.content2:null}</BasicCard>)}

        </Stack>
     
      </Container>
    </SupportTabs>
  )
}
export default TermsAndConditions;