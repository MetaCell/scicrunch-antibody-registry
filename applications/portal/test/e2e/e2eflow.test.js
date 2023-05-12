//IMPORTS:
const puppeteer = require("puppeteer");
const path = require("path");
var scriptName = path.basename(__filename, ".js");
const selectors = require("./selectors");

const antibody_type = require("./submissions.json");

//PAGE INFO:
const baseURL = process.env.APP_URL || "https://www.areg.dev.metacell.us/";
const PAGE_WAIT = 3000;
const TIMEOUT = 60000;


//USERS:
const USERNAME = "metacell-qa";
const PASSWORD = "test";

function range(size, startAt = 0) {
  return Array.from({ length: size }, (_, i) => i + startAt);
}

//TESTS:

jest.setTimeout(300000);

let page;
let browser;

describe("E2E Flow for AntiBody Registry", () => {
  beforeAll(async () => {
    browser = await puppeteer.launch({
      args: [
        "--no-sandbox",
        `--window-size=1600,1000`,
        "--ignore-certificate-errors",
      ],
      headless: true,
      devtools: false,
      defaultViewport: {
        width: 1600,
        height: 1000,
      },
    });

    page = await browser.newPage();
    await page.goto(baseURL);

    await page.waitForFunction(
      () => {
        let el = document.querySelector(".MuiCircularProgress-root");
        return el == null || el.clientHeight === 0;
      },
      { timeout: TIMEOUT }
    );

    await page.waitForSelector(selectors.NAME_ID_FIELD_SELECTOR);

    page.on("response", (response) => {
      const client_server_errors = range(90, 400);
      for (let i = 0; i < client_server_errors.length; i++) {
        expect(response.status()).not.toBe(client_server_errors[i]);
      }
    });
  });

  afterAll(() => {
    browser.close();
  });

  it("HomePage check", async () => {
    console.log("Checking the homepage ...");

    await page.waitForSelector(selectors.DOWNLOAD_SECTION_SELECTOR, {
      disabled: true,
    });
    await page.waitForSelector(selectors.HELP_SELECTOR);
    await page.waitForSelector(selectors.TABLE_SELECTOR);
    const rec_nums = await page.$$eval("h6.MuiTypography-h6", (rec_nums) => {
      return rec_nums.map((rec_num) => rec_num.innerText);
    });

    var lastIndex = rec_nums[0].lastIndexOf(" ");
    const rec_num_str = rec_nums[0].substring(0, lastIndex);

    expect(parseFloat(rec_num_str)).not.toBe("0");

    const update_dates = await page.$$eval(
      "h6.MuiTypography-subtitle1",
      (update_dates) => {
        return update_dates.map((update_date) => update_date.innerText);
      }
    );

    expect(update_dates).not.toContain("Invalid Date");
  });

  it("Perform Search by Catalog Number", async () => {
    console.log("Performing search by Catalog Number ...");

    await page.waitForSelector(selectors.CATALOG_NUMBER_FIELD_SELECTOR);
    const cat_nums = await page.$$eval(
      'div[data-field="catalogNum"]',
      (cat_nums) => {
        return cat_nums.map((cat_num) => cat_num.innerText);
      }
    );
    expect(cat_nums[0]).toBe("Cat Num");
    expect(cat_nums[1]).not.toBeNull;

    await page.click(selectors.SEARCH_BAR_SELECTOR);
    await page.waitForTimeout(3000);
    await page.type(selectors.SEARCH_INPUT_SELECTOR, cat_nums[1]);
    await page.waitForTimeout(2000);
    await page.keyboard.press('Enter')

    await page.waitForFunction(
      () => {
        let el = document.querySelector(".MuiCircularProgress-root");
        return el == null || el.clientHeight === 0;
      },
      { timeout: TIMEOUT }
    );

    await page.waitForTimeout(3000);

    const search_result = await page.$$(
      selectors.CATALOG_NUMBER_FIELD_SELECTOR
    );
    expect(search_result.length).toBeGreaterThanOrEqual(2);

    const rec_nums = await page.$$eval("h6.MuiTypography-h6", (rec_nums) => {
      return rec_nums.map((rec_num) => rec_num.innerText);
    });

    var lastIndex = rec_nums[0].lastIndexOf(" ");

    const rec_num_str = rec_nums[0].substring(0, lastIndex);

    expect(search_result.length - 1).toBe(parseFloat(rec_num_str));

    console.log("Search successful");
  });

  it("Perform Search by other field", async () => {
    console.log("Performing search by Antibody Target ...");

    await page.waitForSelector(selectors.ANTIBPDY_TARGET_FIELD_SELECTOR);
    const targ_antigens = await page.$$eval(
      'div[data-field="abTarget"]',
      (targ_antigens) => {
        return targ_antigens.map((targ_antigen) => targ_antigen.innerText);
      }
    );
    expect(targ_antigens[0]).toBe("Target antigen");
    expect(targ_antigens[1]).not.toBeNull;

    const inputValue = await page.$eval(
      'input[placeholder="Search for catalog number"]',
      (el) => el.value
    );
    await page.click(selectors.SEARCH_INPUT_SELECTOR)
    await page.waitForTimeout(3000);
    for (let i = 0; i < inputValue.length; i++) {
      await page.keyboard.press("Backspace");
    }
    await page.waitForTimeout(2000);
    await page.keyboard.press('Enter')
    await page.waitForTimeout(3000);
    await page.type(selectors.SEARCH_INPUT_SELECTOR, targ_antigens[1]);
    await page.waitForTimeout(2000);
    await page.keyboard.press('Enter')

    await page.waitForFunction(
      () => {
        let el = document.querySelector(".MuiCircularProgress-root");
        return el == null || el.clientHeight === 0;
      },
      { timeout: TIMEOUT }
    );
    await page.waitForTimeout(3000);

    const search_result = await page.$$(
      selectors.ANTIBPDY_TARGET_FIELD_SELECTOR
    );
    expect(search_result.length).toBeGreaterThanOrEqual(2);

    console.log("Search successful");
  });

  it("Log In", async () => {
    console.log("Logging in ...");

    await page.evaluate(() => {
      const elements = Array.from(
        document.querySelectorAll("button.MuiButton-sizeMedium")
      );
      const idElement = elements.find(
        (element) => (element).innerText === "Log in / Register"
      );
      if (idElement) {
        (idElement).click();
      }
    });

    await page.waitForSelector(selectors.USERNAME_SELECTOR, { hidden: false });
    expect(page.url()).toContain("accounts");

    await page.type(
      selectors.USERNAME_SELECTOR,
      process.env.username || USERNAME
    );
    await page.waitForTimeout(3000);
    await page.type(
      selectors.PASSWORD_SELECTOR,
      process.env.password || PASSWORD
    );
    await page.waitForTimeout(3000);

    await page.click(selectors.LOGIN_BUTTON_SELECTOR);

    await page.waitForSelector(selectors.MY_SUBMISSIONS_SELECTOR);

    const user_names = await page.$$eval(
      ".MuiTypography-subtitle2",
      (user_names) => {
        return user_names.map((user_name) => user_name.innerText);
      }
    );

    expect(user_names).not.toBeNull();

    console.log("User logged in");
  });

  it("Submit a Commercial AntiBody", async () => {
    console.log("Submitting Commercial Antibody ...");

    await page.waitForSelector(selectors.ADD_SUBMISSION_SELECTOR);
    await page.click(selectors.ADD_SUBMISSION_SELECTOR);
    await page.waitForTimeout(3000);
    expect(page.url()).toContain("/add");

    await page.waitForSelector(selectors.SUBMISSION_PROGRESS_BAR_SELECTOR);

    await page.click(selectors.NEXT_BUTTON_SELECTOR);

    await page.waitForSelector(selectors.INPUT_URL_SELECTOR);

    await page.type(
      selectors.INPUT_URL_SELECTOR,
      antibody_type.commercial.vendor_product_page
    );
    await page.waitForTimeout(3000);

    await page.waitForSelector(selectors.SUBMIT_SELECTOR, { disabled: true });

    const catalogNumber = Math.floor(100000 + Math.random() * 900000);
    await page.type(
      selectors.INPUT_CATALOG_NUMBER_SELECTOR,
      String(catalogNumber)
    );
    await page.waitForTimeout(3000);
    await page.waitForSelector(
      `iframe[src="${antibody_type.commercial.vendor_product_page}"]`
    );

    await page.type(
      selectors.INPUT_VENDOR_SELECTOR,
      antibody_type.commercial.vendor
    );
    await page.waitForTimeout(3000);

    await page.waitForSelector(selectors.SUBMIT_SELECTOR, { disabled: false });

    await page.type(
      selectors.INPUT_NAME_SELECTOR,
      antibody_type.commercial.antibody_name
    );
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_HOST_SELECTOR,
      antibody_type.commercial.host_species
    );
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_TARGET_SPECIES_SELECTOR,
      antibody_type.commercial.target_reactive_species
    );
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_ANTIBODY_TARGET_SELECTOR,
      antibody_type.commercial.antibody_target
    );
    await page.waitForTimeout(3000);

    await page.click(selectors.CLONALITY_SELECTOR);
    await page.waitForSelector(selectors.CLONALITY_OPTIONS_SELECTOR);
    await page.click(selectors.RECOMBINANT_CLONALITY_SELECTOR);
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_CLONE_ID_SELECTOR,
      antibody_type.commercial.clone_id
    );
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_ISOTYPE_SELECTOR,
      antibody_type.commercial.isotype
    );
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_CONJUGATE_SELECTOR,
      antibody_type.commercial.conjugate
    );
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_FORMAT_SELECTOR,
      antibody_type.commercial.antibody_format
    );
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_UNIPROT_ID_SELECTOR,
      antibody_type.commercial.uniprot_id
    );
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_EPITOPE_SELECTOR,
      antibody_type.commercial.epitope
    );
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_APPLICATIONS_SELECTOR,
      antibody_type.commercial.applications
    );
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_COMMENTS_SELECTOR,
      antibody_type.commercial.comments
    );
    await page.waitForTimeout(3000);

    await page.click(selectors.SUBMIT_SELECTOR);

    await page.waitForTimeout(3000);

    await page.waitForSelector(selectors.SUCCESSFUL_SUBMISSION_SELECTOR);
    await page.waitForTimeout(1000);
    await page.waitForSelector(selectors.CLOSE_SUBMISSION_SELECTOR);
    await page.click(selectors.CLOSE_SUBMISSION_SELECTOR);

    await page.waitForSelector(selectors.TABLE_SELECTOR);
    await page.waitForSelector(selectors.NAME_ID_FIELD_SELECTOR);

    await page.waitForTimeout(3000);

    console.log("Antibody submitted successfully");
  });

  it("Submit a Personal AntiBody", async () => {
    console.log("Submitting Personal Antibody ...");

    await page.waitForSelector(selectors.ADD_SUBMISSION_SELECTOR);
    await page.click(selectors.ADD_SUBMISSION_SELECTOR);
    await page.waitForTimeout(3000);
    expect(page.url()).toContain("/add");

    await page.waitForSelector(selectors.SUBMISSION_PROGRESS_BAR_SELECTOR);
    await page.waitForSelector(selectors.ANTIBODY_TYPE_SELECTOR);

    const antibody_type_buttons = await page.$$(
      "button.MuiCardActionArea-root"
    );
    for (var i = 0; i < antibody_type_buttons.length; i++) {
      await antibody_type_buttons[1].click();
    }

    await page.click(selectors.NEXT_BUTTON_SELECTOR);

    await page.waitForSelector(selectors.INPUT_CATALOG_NUMBER_SELECTOR);

    await page.waitForSelector(selectors.SUBMIT_SELECTOR, { disabled: true });

    const catalogNumber = Math.floor(100000 + Math.random() * 900000);
    await page.type(
      selectors.INPUT_CATALOG_NUMBER_SELECTOR,
      String(catalogNumber)
    );
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_VENDOR_SELECTOR,
      antibody_type.personal.vendor
    );
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_URL_SELECTOR,
      antibody_type.personal.vendor_product_page
    );
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_NAME_SELECTOR,
      antibody_type.personal.antibody_name
    );
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_HOST_SELECTOR,
      antibody_type.personal.host_species
    );
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_TARGET_SPECIES_SELECTOR,
      antibody_type.personal.target_reactive_species
    );
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_ANTIBODY_TARGET_SELECTOR,
      antibody_type.personal.antibody_target
    );
    await page.waitForTimeout(3000);

    await page.click(selectors.CLONALITY_SELECTOR);
    await page.waitForSelector(selectors.CLONALITY_OPTIONS_SELECTOR);
    await page.click(selectors.RECOMBINANT_CLONALITY_SELECTOR);
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_CLONE_ID_SELECTOR,
      antibody_type.personal.clone_id
    );
    await page.waitForTimeout(3000);

    await page.waitForSelector(selectors.SUBMIT_SELECTOR, { disabled: false });

    await page.type(
      selectors.INPUT_ISOTYPE_SELECTOR,
      antibody_type.personal.isotype
    );
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_CONJUGATE_SELECTOR,
      antibody_type.personal.conjugate
    );
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_FORMAT_SELECTOR,
      antibody_type.personal.antibody_format
    );
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_UNIPROT_ID_SELECTOR,
      antibody_type.personal.uniprot_id
    );
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_EPITOPE_SELECTOR,
      antibody_type.personal.epitope
    );
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_APPLICATIONS_SELECTOR,
      antibody_type.personal.applications
    );
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_CITATION_SELECTOR,
      antibody_type.personal.citation
    );
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_COMMENTS_SELECTOR,
      antibody_type.personal.comments
    );
    await page.waitForTimeout(3000);

    await page.click(selectors.SUBMIT_SELECTOR);

    await page.waitForTimeout(3000);

    await page.waitForSelector(selectors.SUCCESSFUL_SUBMISSION_SELECTOR);
    await page.waitForTimeout(1000);
    await page.waitForSelector(selectors.CLOSE_SUBMISSION_SELECTOR);
    await page.click(selectors.CLOSE_SUBMISSION_SELECTOR);

    await page.waitForSelector(selectors.TABLE_SELECTOR);
    await page.waitForSelector(selectors.NAME_ID_FIELD_SELECTOR);

    console.log("Antibody submitted successfully");
  });

  it("Submit a Custom/Other AntiBody", async () => {
    console.log("Submitting Custom Antibody ...");

    await page.waitForSelector(selectors.ADD_SUBMISSION_SELECTOR);
    await page.click(selectors.ADD_SUBMISSION_SELECTOR);
    await page.waitForTimeout(3000);
    expect(page.url()).toContain("/add");

    await page.waitForSelector(selectors.SUBMISSION_PROGRESS_BAR_SELECTOR);
    await page.waitForSelector(selectors.ANTIBODY_TYPE_SELECTOR);

    const antibody_type_buttons = await page.$$(
      "button.MuiCardActionArea-root"
    );
    for (var i = 0; i < antibody_type_buttons.length; i++) {
      await antibody_type_buttons[2].click();
    }

    await page.click(selectors.NEXT_BUTTON_SELECTOR);

    await page.waitForSelector(selectors.INPUT_CATALOG_NUMBER_SELECTOR);

    await page.waitForSelector(selectors.SUBMIT_SELECTOR, { disabled: true });

    const catalogNumber = Math.floor(100000 + Math.random() * 900000);
    await page.type(
      selectors.INPUT_CATALOG_NUMBER_SELECTOR,
      String(catalogNumber)
    );
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_VENDOR_SELECTOR,
      antibody_type.custom.vendor
    );
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_URL_SELECTOR,
      antibody_type.custom.vendor_product_page
    );
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_NAME_SELECTOR,
      antibody_type.custom.antibody_name
    );
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_HOST_SELECTOR,
      antibody_type.custom.host_species
    );
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_TARGET_SPECIES_SELECTOR,
      antibody_type.custom.target_reactive_species
    );
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_ANTIBODY_TARGET_SELECTOR,
      antibody_type.custom.antibody_target
    );
    await page.waitForTimeout(3000);

    await page.click(selectors.CLONALITY_SELECTOR);
    await page.waitForSelector(selectors.CLONALITY_OPTIONS_SELECTOR);
    await page.click(selectors.RECOMBINANT_CLONALITY_SELECTOR);
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_CLONE_ID_SELECTOR,
      antibody_type.custom.clone_id
    );
    await page.waitForTimeout(3000);

    await page.waitForSelector(selectors.SUBMIT_SELECTOR, { disabled: false });

    await page.type(
      selectors.INPUT_ISOTYPE_SELECTOR,
      antibody_type.custom.isotype
    );
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_CONJUGATE_SELECTOR,
      antibody_type.custom.conjugate
    );
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_FORMAT_SELECTOR,
      antibody_type.custom.antibody_format
    );
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_UNIPROT_ID_SELECTOR,
      antibody_type.custom.uniprot_id
    );
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_EPITOPE_SELECTOR,
      antibody_type.custom.epitope
    );
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_APPLICATIONS_SELECTOR,
      antibody_type.custom.applications
    );
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_CITATION_SELECTOR,
      antibody_type.custom.citation
    );
    await page.waitForTimeout(3000);

    await page.type(
      selectors.INPUT_COMMENTS_SELECTOR,
      antibody_type.custom.comments
    );
    await page.waitForTimeout(3000);

    await page.click(selectors.SUBMIT_SELECTOR);

    await page.waitForTimeout(3000);

    await page.waitForSelector(selectors.SUCCESSFUL_SUBMISSION_SELECTOR);

    await page.waitForSelector(selectors.CLOSE_SUBMISSION_SELECTOR);
    await page.click(selectors.CLOSE_SUBMISSION_SELECTOR);
    await page.waitForTimeout(1000);
    await page.waitForSelector(selectors.TABLE_SELECTOR);
    await page.waitForSelector(selectors.NAME_ID_FIELD_SELECTOR);

    console.log("Antibody submitted successfully");
  });

  it("Check AntiBody submissions", async () => {
    console.log("Checking Antibody submissions...");

    await page.waitForSelector(selectors.MY_SUBMISSIONS_SELECTOR);

    const submission_section_buttons = await page.$$("button.MuiTab-labelIcon");
    await submission_section_buttons[1].click();

    await page.waitForSelector(selectors.ANTIBPDY_TARGET_FIELD_SELECTOR);

    await page.waitForFunction(
      () => {
        let el = document.querySelector(".MuiCircularProgress-root");
        return el == null || el.clientHeight === 0;
      },
      { timeout: TIMEOUT }
    );

    await page.click(selectors.FILTER_SELECTOR);
    await page.waitForSelector(selectors.FILTER_TABLE_SELECTOR);
    await page.waitForTimeout(1000);
    await page.evaluate(() => {
      const elements = Array.from(
        document.querySelectorAll(".MuiTypography-body1")
      );
      const idElement = elements.find(
        (element) => (element).innerText === "ID"
      );
      if (idElement) {
        (idElement).click();
      }
    });

    await page.waitForSelector(selectors.ANTIBODY_ID_FIELD_SELECTOR);

    await page.click(selectors.SORT_SELECTOR);
    await page.click(selectors.SORT_SELECTOR);
    await page.waitForTimeout(3000);
    const ab_Target_names = await page.$$eval(
      'div[data-field="abTarget"]',
      (ab_Target_names) => {
        return ab_Target_names.map(
          (ab_Target_name) => ab_Target_name.innerText
        );
      }
    );

    expect(ab_Target_names[1]).toBe("TWIT");
    expect(ab_Target_names[2]).toBe("INST");
    expect(ab_Target_names[3]).toBe("MSN");

    console.log("Antibodies match");
  });

  it("Edit AntiBody submission", async () => {
    await page.waitForTimeout(3000);

    const ID_numbers = await page.$$eval(
      'div[data-field="abId"]',
      (ID_numbers) => {
        return ID_numbers.map((ID_number) => ID_number.innerText);
      }
    );

    await page.click(`a[href= "/update/${ID_numbers[1]}"]`);

    await page.waitForSelector(selectors.INPUT_NAME_SELECTOR, {
      timeout: 15000,
    });
    await page.waitForSelector(selectors.SUBMIT_SELECTOR);

    expect(page.url()).toContain(`update/${ID_numbers[1]}`);

    await page.type(selectors.INPUT_NAME_SELECTOR, " - Edited");

    await page.waitForTimeout(3000);
    await page.click(selectors.SUBMIT_SELECTOR);

    await page.waitForSelector(selectors.ANTIBPDY_TARGET_FIELD_SELECTOR);

    await page.click(selectors.FILTER_SELECTOR);
    await page.waitForSelector(selectors.FILTER_TABLE_SELECTOR);
    await page.waitForTimeout(1000);
    await page.evaluate(() => {
      const elements = Array.from(
        document.querySelectorAll(".MuiTypography-body1")
      );
      const idElement = elements.find(
        (element) => (element).innerText === "ID"
      );
      if (idElement) {
        (idElement).click();
      }
    });

    await page.waitForSelector(selectors.ANTIBODY_ID_FIELD_SELECTOR);

    await page.click(selectors.SORT_SELECTOR);
    await page.click(selectors.SORT_SELECTOR);
    await page.waitForTimeout(3000);

    const nameAndIds = await page.$$eval(
      'div[data-field="nameAndId"]',
      (nameAndIds) => {
        return nameAndIds.map((nameAndId) => nameAndId.innerText);
      }
    );

    expect(nameAndIds[1]).toContain("Edited");
  });

  it("Log out", async () => {
    console.log("Logging out...");

    await page.waitForSelector(selectors.TOP_BUTTONS_SELECTOR);

    const top_buttons = await page.$$(
      "button.MuiButtonBase-root.MuiIconButton-root.MuiIconButton-sizeMedium"
    );
    await top_buttons[1].click();

    await page.waitForSelector(selectors.ACCOUNT_SUBMENU_SELECTOR);

    await page.evaluate(() => {
      const elements = Array.from(
        document.querySelectorAll("li.MuiMenuItem-gutters")
      );
      const idElement = elements.find(
        (element) => (element).innerText === "Log out"
      );
      if (idElement) {
        (idElement).click();
      }
    });

    await page.waitForSelector(selectors.NAME_ID_FIELD_SELECTOR);

    console.log("User logged out");
  });
});

