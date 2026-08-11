//IMPORTS:
const puppeteer = require("puppeteer");
const path = require("path");
var scriptName = path.basename(__filename, ".js");
const s = require("./selectors");


//PAGE INFO:
const baseURL = process.env.APP_URL || "https://www.areg.dev.metacell.us/";
const PAGE_WAIT = 3000;
const TIMEOUT = 1000;
// The grid only re-renders once the search response is in, so give the spinner
// room to clear on a cold query instead of racing it.
const LOADER_TIMEOUT = 60000;

// page.waitForTimeout was removed in puppeteer 22.
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

// The record count is rendered with locale thousands separators ("2,803"), and
// parseFloat stops at the comma: it would read that as 2.
function parseCount(text) {
  return parseInt(String(text).replace(/[^\d]/g, ""), 10);
}

//TESTS:

jest.setTimeout(300000);

let page;
let browser;
let httpErrors = [];



async function waitLoaderToDisappear() {
  // The spinner takes a moment to show up, and for a warm response it may not
  // show up at all, so its appearance is best effort...
  try {
    await page.waitForSelector(s.PROGRESS_LOADER, { timeout: TIMEOUT });
  } catch(e) {
    console.log("No loader found");
  }
  // ...but it has to be gone before the table can be read back: the row cells
  // and the record count are rewritten only when loading completes, so reading
  // them while the spinner is still up mixes the new count with the previous
  // search's rows.
  await page.waitForSelector(s.PROGRESS_LOADER, {
    hidden: true,
    timeout: LOADER_TIMEOUT,
  });
  try {
    await page.waitForSelector(s.CATALOG_NUMBER_FIELD, { timeout: TIMEOUT });
  } catch(e) {
    console.log("No table results found");
  }

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

describe("E2E Flow for AntiBody Registry", () => {

  

  async function getRecordNumber() {
    return getValue(s.RECORD_NUMBER);
  }
  
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

    await waitLoaderToDisappear()

    await page.waitForSelector(s.NAME_ID_FIELD);

    // Only collected here: asserting inside the listener attributes the failure
    // to whichever test happens to be running when the response arrives.
    page.on("response", (response) => {
      if (response.status() >= 400) {
        httpErrors.push(`${response.status()} ${response.url()}`);
      }
    });
  });

  afterEach(() => {
    const errors = httpErrors;
    httpErrors = [];
    expect(errors).toEqual([]);
  });

  afterAll(async () => {
    await browser.close();
  });

  it("HomePage check", async () => {
    console.log("Checking the homepage ...");

    await page.waitForSelector(s.DOWNLOAD_SECTION, {
      disabled: true,
    });
    await page.waitForSelector(s.HELP);
    await page.waitForSelector(s.TABLE);
    const rec_num_str = await getRecordNumber();

    expect(parseCount(rec_num_str)).not.toBe(0);

    const update_date = await getValue(s.UPDATE_DATE);

    expect(update_date).not.toContain("Invalid Date");

    
  });

  it("Perform Search by Catalog Number", async () => {
    console.log("Performing search by Catalog Number ...");

    await page.waitForSelector(s.CATALOG_NUMBER_FIELD);
    const cat_nums = await getValues(s.CATALOG_NUMBER_FIELD);
    expect(cat_nums[0]).toBe("Cat Num");
    expect(cat_nums[1]).not.toBeNull;

    await page.click(s.SEARCH_BAR);

    await page.type(s.SEARCH_INPUT, cat_nums[1]);

    await page.keyboard.press('Enter')

    await waitLoaderToDisappear();



    const search_result = await page.$$(
      s.CATALOG_NUMBER_FIELD
    );
    expect(search_result.length).toBeGreaterThanOrEqual(2);

    const rec_num_str = await getRecordNumber();

    // search_result counts the header cell on top of one cell per row.
    expect(parseCount(rec_num_str)).toBeGreaterThanOrEqual(search_result.length - 1);

    console.log("Search successful");
  });

  it("Perform Search by other field", async () => {
    console.log("Performing search by Antibody Target ...");

    await page.waitForSelector(s.ANTIBODY_TARGET_FIELD);
    const targAntigens = await getValues(s.ANTIBODY_TARGET_FIELD);
     
    expect(targAntigens[0]).toBe("Target antigen");
    expect(targAntigens[1]).not.toBeNull;
    await page.waitForSelector(s.SEARCH_INPUT);
    const inputValue = await getValue(s.SEARCH_INPUT);
    console.log("inputValue", inputValue);

    await page.click(s.SEARCH_INPUT)

    await page.waitForSelector(s.SEARCH_DELETE_BUTTON);

    await page.click(s.SEARCH_DELETE_BUTTON)
  
    await page.keyboard.press('Enter')
    console.log("targAntigens", targAntigens);
    
    await page.type(s.SEARCH_INPUT, targAntigens[1]);

    await page.keyboard.press('Enter')

    // Clearing the search box above fires a query of its own: let that one start
    // and finish before waiting on the spinner for this search, or the wait can
    // return in the gap between the two.
    await sleep(PAGE_WAIT);

    await waitLoaderToDisappear();


    const search_result = await getValues(s.ANTIBODY_TARGET_FIELD);
    expect(search_result.length).toBeGreaterThanOrEqual(2);

    console.log("Search successful");
  });

  
});


