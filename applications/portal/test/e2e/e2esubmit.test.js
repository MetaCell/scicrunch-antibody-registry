//IMPORTS:
const puppeteer = require("puppeteer");
const path = require("path");
var scriptName = path.basename(__filename, ".js");
const selectors = require("./selectors");

const antibody_type = require("./submissions.json");

//PAGE INFO:
const baseURL = process.env.APP_URL || "https://www.areg.dev.metacell.us";
// Third-party calls the page happens to make are not this suite's business: an
// enrichment or analytics service returning 429 says nothing about the app. The
// login step asserts its own outcome, so skipping the accounts host is fine too.
const appOrigin = new URL(baseURL).origin;
const PAGE_WAIT = 3000;
// Keycloak has to redirect back and the app has to boot before the user menu
// shows up, so this covers a full round trip rather than a single render.
const LOGIN_TIMEOUT = 60000;
// An update is a write plus a redirect plus a grid reload, so it needs more room
// than the 30s puppeteer default.
const UPDATE_TIMEOUT = 60000;


//USERS:
// Injected by the pipeline from harness.accounts.users - uppercase names are the
// cloud-harness convention, see cloudharness_utils.testing.util.
// Fallbacks match harness.accounts.users in applications/portal/deploy/values-dev.yaml
// so a local run against dev works without setting anything.
const USERNAME = process.env.USERNAME || "metacell-qa@testuser.com";
const PASSWORD = process.env.PASSWORD || "test";

// page.waitForTimeout was removed in puppeteer 22.
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

//TESTS:

jest.setTimeout(300000);

let page;
let browser;
let httpErrors = [];
let alerts = [];
let loggedIn = false;

// Everything after the login step acts as a signed-in user. Without this each of
// them waits out its own 30s timeout on a selector that cannot appear, which
// buries the one failure that actually matters.
function requireLogin() {
  if (!loggedIn) {
    throw new Error("Skipped: the login step did not succeed, see its failure above");
  }
}

async function click(selector) {
  // Waiting here keeps a missing element reported as the selector it is, rather
  // than as "cannot read properties of null" further down.
  await page.waitForSelector(selector);
  const element = await page.$(selector);
  const value = await element.evaluate((el) => el.click());
  return value;
}

async function getValue(selector) {
  const element = await page.$(selector);
  const value = await page.evaluate((el) => el.innerText, element);
  return value;
}

async function getValues(selector) {
  const elements = await page.$$(selector);
  const values = [];
  for(const element of elements) {
    values.push(await page.evaluate(e => e.innerText, element));
  }
  return values;
}

// Resolves with null once the app is reached, or with a description of what went
// wrong instead. Without this a rejected login just times out on every app
// selector further down, which hides the actual cause.
async function waitForLoginOutcome() {
  const never = () => new Promise(() => {});
  const reachedApp = page
    .waitForSelector(selectors.USER_MENU, { timeout: LOGIN_TIMEOUT })
    .then(() => null)
    .catch(never);
  const rejected = page
    .waitForSelector(selectors.KC_LOGIN_ERROR, { timeout: LOGIN_TIMEOUT })
    .then((el) => el.evaluate((e) => e.innerText))
    .catch(never);
  return Promise.race([
    reachedApp,
    rejected,
    sleep(LOGIN_TIMEOUT).then(() => "timed out before the app loaded"),
  ]);
}

describe("E2E Flow for AntiBody Registry", () => {
  beforeAll(async () => {
    browser = await puppeteer.launch({
      args: [
        "--no-sandbox",
        `--window-size=1600,1000`,
        "--ignore-certificate-errors",
      ],
      headless: !process.env.PUPPETEER_DISPLAY,
      devtools: false,
      defaultViewport: {
        width: 1600,
        height: 1000,
      },
    });

    page = await browser.newPage();
    await page.goto(baseURL);

    await page.waitForSelector(selectors.NAME_ID_FIELD);

    // Only collected here: asserting inside the listener attributes the failure
    // to whichever test happens to be running when the response arrives.
    page.on("response", (response) => {
      if (response.status() >= 400 && response.url().startsWith(appOrigin)) {
        httpErrors.push(`${response.status()} ${response.url()}`);
      }
    });

    // Registering a handler stops the browser dismissing dialogs for us, so
    // dismiss explicitly - the point is to keep the message for the failure text.
    page.on("dialog", async (dialog) => {
      alerts.push(`${dialog.type()}: ${dialog.message()}`);
      await dialog.dismiss();
    });
  });

  afterEach(() => {
    const errors = httpErrors;
    httpErrors = [];
    alerts = [];
    expect(errors).toEqual([]);
  });

  afterAll(async () => {
    await browser.close();
  });


  it("Log In", async () => {
    console.log("Logging in ...");

    await click(selectors.LOGIN_BUTTON)

    await page.waitForSelector(selectors.KC_USERNAME, { hidden: false });
    expect(page.url()).toContain("accounts");

    await page.type(selectors.KC_USERNAME, USERNAME);

    await page.type(selectors.KC_PASSWORD, PASSWORD);


    await page.click(selectors.KC_LOGIN_BUTTON);

    const failure = await waitForLoginOutcome();
    if (failure) {
      throw new Error(`Login as "${USERNAME}" did not reach the app: ${failure}`);
    }

    await page.waitForSelector(selectors.MY_SUBMISSIONS);

    loggedIn = true;
    console.log("User logged in");
  });

  it("Submit a Commercial AntiBody", async () => {
    requireLogin();
    console.log("Submitting Commercial Antibody ...");

    await page.waitForSelector(selectors.ADD_SUBMISSION);
    await page.click(selectors.ADD_SUBMISSION);

    expect(page.url()).toContain("/add");

    await page.waitForSelector(selectors.SUBMISSION_PROGRESS_BAR);

    await page.click(selectors.NEXT_BUTTON);

    await page.waitForSelector(selectors.INPUT_URL);

    await page.type(
      selectors.INPUT_URL,
      antibody_type.commercial.vendor_product_page
    );

    await page.waitForSelector(selectors.SUBMIT, { disabled: true });

    const catalogNumber = Math.floor(100000 + Math.random() * 900000);

    await page.type(
      selectors.INPUT_CATALOG_NUMBER,
      String(catalogNumber)
    );

    await page.waitForSelector(
      `iframe[src="${antibody_type.commercial.vendor_product_page}"]`
    );

    await page.type(
      selectors.INPUT_VENDOR,
      antibody_type.commercial.vendor
    );


    await page.waitForSelector(selectors.SUBMIT, { disabled: false });

    await page.type(
      selectors.INPUT_NAME,
      antibody_type.commercial.antibody_name
    );
    await page.waitForSelector(selectors.INPUT_HOST);

    await page.type(
      selectors.INPUT_HOST,
      antibody_type.commercial.host_species
    );
    await page.waitForSelector(selectors.INPUT_TARGET_SPECIES);

    await page.type(
      selectors.INPUT_TARGET_SPECIES,
      antibody_type.commercial.target_reactive_species
    );
    await page.waitForSelector(selectors.INPUT_ANTIBODY_TARGET);

    await page.type(
      selectors.INPUT_ANTIBODY_TARGET,
      antibody_type.commercial.antibody_target
    );
    await page.waitForSelector(selectors.CLONALITY);

    await page.click(selectors.CLONALITY);
    await page.waitForSelector(selectors.CLONALITY_OPTIONS);
    await page.click(selectors.RECOMBINANT_CLONALITY);
    await page.waitForSelector(selectors.INPUT_CLONE_ID);

    await page.type(
      selectors.INPUT_CLONE_ID,
      antibody_type.commercial.clone_id
    );
    await page.waitForSelector(selectors.INPUT_ISOTYPE);

    await page.type(
      selectors.INPUT_ISOTYPE,
      antibody_type.commercial.isotype
    );
    await page.waitForSelector(selectors.INPUT_CONJUGATE);

    await page.type(
      selectors.INPUT_CONJUGATE,
      antibody_type.commercial.conjugate
    );
    await page.waitForSelector(selectors.INPUT_FORMAT);

    await page.type(
      selectors.INPUT_FORMAT,
      antibody_type.commercial.antibody_format
    );
    await page.waitForSelector(selectors.INPUT_UNIPROT_ID);

    await page.type(
      selectors.INPUT_UNIPROT_ID,
      antibody_type.commercial.uniprot_id
    );
    await page.waitForSelector(selectors.INPUT_EPITOPE);

    await page.type(
      selectors.INPUT_EPITOPE,
      antibody_type.commercial.epitope
    );
    await page.waitForSelector(selectors.INPUT_APPLICATIONS);

    await page.type(
      selectors.INPUT_APPLICATIONS,
      antibody_type.commercial.applications
    );
    await page.waitForSelector(selectors.INPUT_COMMENTS);

    await page.type(
      selectors.INPUT_COMMENTS,
      antibody_type.commercial.comments
    );
    await page.waitForSelector(selectors.SUBMIT);

    await page.click(selectors.SUBMIT);

    await page.waitForSelector(selectors.SUCCESSFUL_SUBMISSION);
    await page.waitForSelector(selectors.CLOSE_SUBMISSION);
    await page.click(selectors.CLOSE_SUBMISSION);

    await page.waitForSelector(selectors.TABLE);
    await page.waitForSelector(selectors.NAME_ID_FIELD);

    console.log("Antibody submitted successfully");
  });

  it("Submit a Personal AntiBody", async () => {
    requireLogin();
    console.log("Submitting Personal Antibody ...");

    await page.waitForSelector(selectors.ADD_SUBMISSION);
    await page.click(selectors.ADD_SUBMISSION);  

    await page.waitForSelector(selectors.SUBMISSION_PROGRESS_BAR);
    expect(page.url()).toContain("/add");
    await page.waitForSelector(selectors.ANTIBODY_TYPE);

    const antibody_type_buttons = await page.$$(
      "button.MuiCardActionArea-root"
    );
    for (var i = 0; i < antibody_type_buttons.length; i++) {
      await antibody_type_buttons[1].click();
    }

    await page.click(selectors.NEXT_BUTTON);

    await page.waitForSelector(selectors.INPUT_CATALOG_NUMBER);

    await page.waitForSelector(selectors.SUBMIT, { disabled: true });

    const catalogNumber = Math.floor(100000 + Math.random() * 900000);
    await page.type(
      selectors.INPUT_CATALOG_NUMBER,
      String(catalogNumber)
    );
    await page.waitForSelector(selectors.INPUT_VENDOR);

    await page.type(
      selectors.INPUT_VENDOR,
      antibody_type.personal.vendor
    );
    await page.waitForSelector(selectors.INPUT_URL);

    await page.type(
      selectors.INPUT_URL,
      antibody_type.personal.vendor_product_page
    );
    await page.waitForSelector(selectors.INPUT_NAME);

    await page.type(
      selectors.INPUT_NAME,
      antibody_type.personal.antibody_name
    );
    await page.waitForSelector(selectors.INPUT_NAME);

    await page.type(
      selectors.INPUT_HOST,
      antibody_type.personal.host_species
    );
    await page.waitForSelector(selectors.INPUT_HOST);

    await page.type(
      selectors.INPUT_TARGET_SPECIES,
      antibody_type.personal.target_reactive_species
    );
    await page.waitForSelector(selectors.INPUT_TARGET_SPECIES);

    await page.type(
      selectors.INPUT_ANTIBODY_TARGET,
      antibody_type.personal.antibody_target
    );
    await page.waitForSelector(selectors.CLONALITY);

    await page.click(selectors.CLONALITY);
    await page.waitForSelector(selectors.CLONALITY_OPTIONS);
    await page.click(selectors.RECOMBINANT_CLONALITY);
    await page.waitForSelector(selectors.INPUT_CLONE_ID);

    await page.type(
      selectors.INPUT_CLONE_ID,
      antibody_type.personal.clone_id
    );

    await page.waitForSelector(selectors.SUBMIT, { disabled: false });

    await page.type(
      selectors.INPUT_ISOTYPE,
      antibody_type.personal.isotype
    );
    await page.waitForSelector(selectors.INPUT_CONJUGATE);

    await page.type(
      selectors.INPUT_CONJUGATE,
      antibody_type.personal.conjugate
    );
    await page.waitForSelector(selectors.INPUT_FORMAT);

    await page.type(
      selectors.INPUT_FORMAT,
      antibody_type.personal.antibody_format
    );
    await page.waitForSelector(selectors.INPUT_UNIPROT_ID);

    await page.type(
      selectors.INPUT_UNIPROT_ID,
      antibody_type.personal.uniprot_id
    );
    await page.waitForSelector(selectors.INPUT_EPITOPE);

    await page.type(
      selectors.INPUT_EPITOPE,
      antibody_type.personal.epitope
    );
    await page.waitForSelector(selectors.INPUT_APPLICATIONS);

    await page.type(
      selectors.INPUT_APPLICATIONS,
      antibody_type.personal.applications
    );
    await page.waitForSelector(selectors.INPUT_CITATION);

    await page.type(
      selectors.INPUT_CITATION,
      antibody_type.personal.citation
    );
    await page.waitForSelector(selectors.INPUT_COMMENTS);

    await page.type(
      selectors.INPUT_COMMENTS,
      antibody_type.personal.comments
    );
    await page.waitForSelector(selectors.SUBMIT);

    await page.click(selectors.SUBMIT);

    await page.waitForSelector(selectors.SUCCESSFUL_SUBMISSION);

    await page.waitForSelector(selectors.CLOSE_SUBMISSION);
    await page.click(selectors.CLOSE_SUBMISSION);

    await page.waitForSelector(selectors.TABLE);
    await page.waitForSelector(selectors.NAME_ID_FIELD);

    console.log("Antibody submitted successfully");
  });

  it("Submit a Custom/Other AntiBody", async () => {
    requireLogin();
    console.log("Submitting Custom Antibody ...");

    await page.waitForSelector(selectors.ADD_SUBMISSION);
    await page.click(selectors.ADD_SUBMISSION);
    await page.waitForSelector(selectors.SUBMISSION_PROGRESS_BAR);
    expect(page.url()).toContain("/add");
    await page.waitForSelector(selectors.ANTIBODY_TYPE);

    const antibody_type_buttons = await page.$$(
      "button.MuiCardActionArea-root"
    );
    for (var i = 0; i < antibody_type_buttons.length; i++) {
      await antibody_type_buttons[2].click();
    }

    await page.click(selectors.NEXT_BUTTON);

    await page.waitForSelector(selectors.INPUT_CATALOG_NUMBER);

    await page.waitForSelector(selectors.SUBMIT, { disabled: true });

    const catalogNumber = Math.floor(100000 + Math.random() * 900000);
    await page.type(
      selectors.INPUT_CATALOG_NUMBER,
      String(catalogNumber)
    );
    await page.waitForSelector(selectors.INPUT_VENDOR);

    await page.type(
      selectors.INPUT_VENDOR,
      antibody_type.custom.vendor
    );
    await page.waitForSelector(selectors.INPUT_URL);

    await page.type(
      selectors.INPUT_URL,
      antibody_type.custom.vendor_product_page
    );
    await page.waitForSelector(selectors.INPUT_NAME);

    await page.type(
      selectors.INPUT_NAME,
      antibody_type.custom.antibody_name
    );
    await page.waitForSelector(selectors.INPUT_HOST);

    await page.type(
      selectors.INPUT_HOST,
      antibody_type.custom.host_species
    );
    await page.waitForSelector(selectors.INPUT_TARGET_SPECIES);

    await page.type(
      selectors.INPUT_TARGET_SPECIES,
      antibody_type.custom.target_reactive_species
    );
    await page.waitForSelector(selectors.INPUT_ANTIBODY_TARGET);

    await page.type(
      selectors.INPUT_ANTIBODY_TARGET,
      antibody_type.custom.antibody_target
    );
    await page.waitForSelector(selectors.CLONALITY);

    await page.click(selectors.CLONALITY);
    await page.waitForSelector(selectors.CLONALITY_OPTIONS);
    await page.click(selectors.RECOMBINANT_CLONALITY);
    await page.waitForSelector(selectors.INPUT_CLONE_ID);

    await page.type(
      selectors.INPUT_CLONE_ID,
      antibody_type.custom.clone_id
    );

    await page.waitForSelector(selectors.SUBMIT, { disabled: false });

    await page.type(
      selectors.INPUT_ISOTYPE,
      antibody_type.custom.isotype
    );
    await page.waitForSelector(selectors.INPUT_CONJUGATE);

    await page.type(
      selectors.INPUT_CONJUGATE,
      antibody_type.custom.conjugate
    );
    await page.waitForSelector(selectors.INPUT_FORMAT);

    await page.type(
      selectors.INPUT_FORMAT,
      antibody_type.custom.antibody_format
    );
    await page.waitForSelector(selectors.INPUT_UNIPROT_ID);

    await page.type(
      selectors.INPUT_UNIPROT_ID,
      antibody_type.custom.uniprot_id
    );
    await page.waitForSelector(selectors.INPUT_EPITOPE);

    await page.type(
      selectors.INPUT_EPITOPE,
      antibody_type.custom.epitope
    );
    await page.waitForSelector(selectors.INPUT_APPLICATIONS);

    await page.type(
      selectors.INPUT_APPLICATIONS,
      antibody_type.custom.applications
    );
    await page.waitForSelector(selectors.INPUT_CITATION);

    await page.type(
      selectors.INPUT_CITATION,
      antibody_type.custom.citation
    );
    await page.waitForSelector(selectors.INPUT_COMMENTS);

    await page.type(
      selectors.INPUT_COMMENTS,
      antibody_type.custom.comments
    );
    await page.waitForSelector(selectors.SUBMIT);

    await page.click(selectors.SUBMIT);

    await page.waitForSelector(selectors.SUCCESSFUL_SUBMISSION);

    await page.waitForSelector(selectors.CLOSE_SUBMISSION);
    await page.click(selectors.CLOSE_SUBMISSION);
    await page.waitForSelector(selectors.TABLE);
    await page.waitForSelector(selectors.NAME_ID_FIELD);

    console.log("Antibody submitted successfully");
  });

  // it("Check AntiBody submissions", async () => {
  //   console.log("Checking Antibody submissions...");

  //   await page.waitForSelector(selectors.MY_SUBMISSIONS);
  //   click(selectors.MY_SUBMISSIONS);

  //   await page.waitForSelector(selectors.ANTIBODY_TARGET_FIELD);



  //   const ab_Target_names = await getValues(selectors.ANTIBODY_TARGET_FIELD);
  //   expect(ab_Target_names.find(e => e === "TWIT")).toBeTruthy();
  //   expect(ab_Target_names.find(e => e === "INST")).toBeTruthy();
  //   expect(ab_Target_names.find(e => e === "MSN")).toBeTruthy();

  //   console.log("Antibodies match");
  // });

  it("Edit AntiBody submission", async () => {
    requireLogin();
    await click(selectors.MY_SUBMISSIONS);
    await page.waitForSelector(selectors.ANTIBODY_NAME_ID_FIELD);
  
    const idNames = await getValues(selectors.ANTIBODY_NAME_ID_FIELD);
    console.log(idNames[0]);
    await page.goto(`${baseURL}/update/${idNames[1].split("AB_")[1]}`);

    await page.waitForSelector(selectors.INPUT_NAME, {
      timeout: 15000,
    });
    await page.waitForSelector(selectors.SUBMIT);


    await page.type(selectors.INPUT_NAME, " - Edited");

    await page.waitForSelector(selectors.SUBMIT);
    await page.click(selectors.SUBMIT);

    // UpdateForm pushes /submissions on success and reports failure with a native
    // alert(), which the browser dismisses without the test ever seeing it. Wait
    // on the navigation rather than the grid so a failed update reports the app's
    // own error instead of an unexplained selector timeout.
    await page
      .waitForFunction(() => location.pathname === "/submissions", {
        timeout: UPDATE_TIMEOUT,
      })
      .catch(() => {
        throw new Error(
          `The update did not complete: ${
            alerts.length ? alerts.join("; ") : "the app reported no error"
          }`
        );
      });

    await page.waitForSelector(selectors.ANTIBODY_NAME_ID_FIELD);


    const nameAndIds = await getValues(selectors.ANTIBODY_NAME_ID_FIELD);

    // expect(nameAndIds.find(n => n.includes("Edited"))).toBeTruthy();
  });

  it("Log out", async () => {
    requireLogin();
    console.log("Logging out...");

    await page.waitForSelector(selectors.TOP_BUTTONS);

    await click('.btn-user-menu');

    await page.waitForSelector('.btn-logout');

    await click('.btn-logout');


    console.log("User logged out");
  });
});

