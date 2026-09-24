import os
import sys
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


# ============================================================
# CONFIGURATION
# ============================================================

EMAIL = "sandeepnaidusukara@gmail.com"
PASSWORD = "Sandeep@123"

RESUME_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "sandeep_java_fullstack_Aws_developer_2_8_years.pdf"
)


# ============================================================
# DIAGNOSTICS
# ============================================================

def print_page_diagnostics(page):
    print("\n========== PAGE DIAGNOSTICS ==========")

    print("URL:", page.url)

    try:
        print("TITLE:", page.title())
    except Exception:
        print("TITLE: <unable to read>")

    print("\nInputs found:")

    try:
        inputs = page.locator("input")
        count = inputs.count()

        print("Input count:", count)

        for i in range(count):
            inp = inputs.nth(i)

            print(
                f"[{i}] "
                f"type={inp.get_attribute('type')} | "
                f"name={inp.get_attribute('name')} | "
                f"id={inp.get_attribute('id')} | "
                f"placeholder={inp.get_attribute('placeholder')} | "
                f"autocomplete={inp.get_attribute('autocomplete')}"
            )

    except Exception as e:
        print("Could not inspect inputs:", e)

    print("\nButtons found:")

    try:
        buttons = page.locator("button")
        count = buttons.count()

        print("Button count:", count)

        for i in range(min(count, 20)):
            button = buttons.nth(i)

            try:
                text = button.inner_text().strip()
            except Exception:
                text = ""

            print(
                f"[{i}] "
                f"text={text[:100]!r} | "
                f"type={button.get_attribute('type')}"
            )

    except Exception as e:
        print("Could not inspect buttons:", e)

    print("\nBody text preview:")

    try:
        body_text = page.locator("body").inner_text()
        body_text = " ".join(body_text.split())

        print(body_text[:2000])

    except Exception as e:
        print("Could not read body text:", e)

    print("======================================\n")


# ============================================================
# FIND EMAIL FIELD
# ============================================================

def find_email_field(page):

    selectors = [
        "#usernameField",
        "input[name='username']",
        "input[name='email']",
        "input[type='email']",
        "input[placeholder*='Email' i]",
        "input[placeholder*='email' i]",
        "input[placeholder*='username' i]",
    ]

    for selector in selectors:

        try:
            locator = page.locator(selector).first

            locator.wait_for(
                state="visible",
                timeout=5000
            )

            print("Email field found using:", selector)

            return locator

        except PlaywrightTimeoutError:
            continue

        except Exception:
            continue

    return None


# ============================================================
# FIND PASSWORD FIELD
# ============================================================

def find_password_field(page):

    selectors = [
        "#passwordField",
        "input[name='password']",
        "input[type='password']",
    ]

    for selector in selectors:

        try:
            locator = page.locator(selector).first

            locator.wait_for(
                state="visible",
                timeout=5000
            )

            print("Password field found using:", selector)

            return locator

        except PlaywrightTimeoutError:
            continue

        except Exception:
            continue

    return None


# ============================================================
# FIND LOGIN BUTTON
# ============================================================

def find_login_button(page):

    selectors = [
        "button:has-text('Login')",
        "button[type='submit']",
        "input[type='submit']",
        "[role='button']:has-text('Login')",
    ]

    for selector in selectors:

        try:
            locator = page.locator(selector).first

            locator.wait_for(
                state="visible",
                timeout=5000
            )

            print("Login button found using:", selector)

            return locator

        except PlaywrightTimeoutError:
            continue

        except Exception:
            continue

    return None


# ============================================================
# LOGIN
# ============================================================

def login(page):

    print("1/9 Opening Naukri login page...")

    page.goto(
        "https://www.naukri.com/nlogin/login",
        wait_until="domcontentloaded",
        timeout=60000
    )

    page.wait_for_timeout(5000)

    print("Current URL:", page.url)

    print("2/9 Finding email field...")

    email_field = find_email_field(page)

    if email_field is None:

        print("\nEmail field was NOT found.")

        print_page_diagnostics(page)

        raise RuntimeError(
            "Naukri email field was not found. "
            "The page returned by Naukri does not contain the expected login form."
        )

    email_field.fill(EMAIL)

    print("Email entered.")

    print("3/9 Finding password field...")

    password_field = find_password_field(page)

    if password_field is None:

        print("\nPassword field was NOT found.")

        print_page_diagnostics(page)

        raise RuntimeError(
            "Naukri password field was not found."
        )

    password_field.fill(PASSWORD)

    print("Password entered.")

    print("4/9 Finding Login button...")

    login_button = find_login_button(page)

    if login_button is None:

        print("\nLogin button was NOT found.")

        print_page_diagnostics(page)

        raise RuntimeError(
            "Naukri Login button was not found."
        )

    login_button.click()

    print("Login button clicked.")

    page.wait_for_timeout(7000)

    print("After login URL:", page.url)

    return True


# ============================================================
# OPEN PROFILE
# ============================================================

def open_profile(page):

    print("5/9 Navigating to Naukri profile...")

    page.goto(
        "https://www.naukri.com/mnjuser/profile",
        wait_until="domcontentloaded",
        timeout=60000
    )

    page.wait_for_timeout(5000)

    print("Profile URL:", page.url)

    # If we were redirected back to login, login didn't succeed.
    if "nlogin" in page.url.lower():

        print_page_diagnostics(page)

        raise RuntimeError(
            "Naukri redirected back to the login page. "
            "Login was not completed."
        )


# ============================================================
# FIND RESUME FILE INPUT
# ============================================================

def find_file_input(page):

    print("6/9 Looking for resume upload input...")

    selectors = [
        "input[type='file']",
        "input[accept*='pdf' i]",
        "input[accept*='document' i]",
    ]

    for selector in selectors:

        try:

            locator = page.locator(selector).first

            if locator.count() > 0:

                print(
                    "File input found using:",
                    selector
                )

                return locator

        except Exception:
            continue

    return None


# ============================================================
# UPLOAD RESUME
# ============================================================

def upload_resume(page):

    print("7/9 Uploading resume...")

    if not os.path.exists(RESUME_PATH):

        raise FileNotFoundError(
            f"Resume file not found: {RESUME_PATH}"
        )

    print("Resume path:", RESUME_PATH)

    file_input = find_file_input(page)

    if file_input is None:

        print("\nResume file input was not found.")

        print_page_diagnostics(page)

        raise RuntimeError(
            "Naukri resume file input was not found."
        )

    file_input.set_input_files(RESUME_PATH)

    print("Resume file selected successfully.")

    page.wait_for_timeout(5000)


# ============================================================
# MAIN
# ============================================================

def login_and_upload(headless=True):

    if not EMAIL or EMAIL == "YOUR_NAUKRI_EMAIL":

        raise RuntimeError(
            "Please set your Naukri email in main.py."
        )

    if not PASSWORD or PASSWORD == "YOUR_NEW_NAUKRI_PASSWORD":

        raise RuntimeError(
            "Please set your Naukri password in main.py."
        )

    if not os.path.exists(RESUME_PATH):

        raise FileNotFoundError(
            f"Resume not found: {RESUME_PATH}"
        )

    print("=" * 55)
    print("        NAUKRI RESUME AUTO UPLOADER")
    print("=" * 55)
    print(
        "Mode:",
        "GitHub Actions / Headless"
        if headless
        else "Local / Visible"
    )
    print("Resume:", os.path.basename(RESUME_PATH))
    print("=" * 55)

    with sync_playwright() as p:

        print("\nStarting Chromium...")

        browser = p.chromium.launch(
            headless=headless
        )

        context = browser.new_context(
            viewport={
                "width": 1280,
                "height": 800
            }
        )

        page = context.new_page()

        try:

            # ------------------------------------------------
            # LOGIN
            # ------------------------------------------------

            login(page)

            # ------------------------------------------------
            # PROFILE
            # ------------------------------------------------

            open_profile(page)

            # ------------------------------------------------
            # UPLOAD
            # ------------------------------------------------

            upload_resume(page)

            # ------------------------------------------------
            # FINISH
            # ------------------------------------------------

            print("8/9 Upload process completed.")

            page.wait_for_timeout(3000)

            print("Current URL:", page.url)

            print("9/9 DONE!")

        finally:

            browser.close()

            print("\nBrowser closed.")

    print("=" * 55)
    print("        PROCESS FINISHED")
    print("=" * 55)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    headless = "--headless" in sys.argv

    login_and_upload(
        headless=headless
    )