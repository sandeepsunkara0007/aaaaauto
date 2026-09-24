import os
import sys
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


# ============================================================
# Naukri Credentials
# ============================================================

EMAIL = "sandeepnaidusukara@gmail.com"
PASSWORD = "Sandeep@123"


# ============================================================
# Resume
# ============================================================

RESUME_PATH = os.path.join(
    os.path.dirname(__file__),
    "sandeep_java_fullstack_Aws_developer_2_8_years.pdf"
)


def login_and_upload(headless=False):

    if not os.path.exists(RESUME_PATH):
        raise FileNotFoundError(
            f"Resume not found: {RESUME_PATH}"
        )

    with sync_playwright() as p:

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

        # ====================================================
        # 1. Open Login
        # ====================================================

        print("1/9 Opening Naukri login page...")

        page.goto(
            "https://www.naukri.com/nlogin/login",
            wait_until="domcontentloaded",
            timeout=60000
        )

        page.wait_for_timeout(5000)

        print("Current URL:", page.url)

        # ====================================================
        # 2. Email
        # ====================================================

        print("2/9 Entering email...")

        email_selectors = [
            "#usernameField",
            "input[name='username']",
            "input[type='email']",
            "input[placeholder*='Email']",
            "input[placeholder*='email']"
        ]

        email_field = None

        for selector in email_selectors:
            try:
                locator = page.locator(selector).first

                if locator.is_visible(timeout=3000):
                    email_field = locator
                    print(
                        f"Email field found: {selector}"
                    )
                    break

            except PlaywrightTimeoutError:
                continue

        if email_field is None:
            raise RuntimeError(
                "Naukri email field was not found."
            )

        email_field.fill(EMAIL)

        # ====================================================
        # 3. Password
        # ====================================================

        print("3/9 Entering password...")

        password_selectors = [
            "#passwordField",
            "input[name='password']",
            "input[type='password']"
        ]

        password_field = None

        for selector in password_selectors:
            try:
                locator = page.locator(selector).first

                if locator.is_visible(timeout=3000):
                    password_field = locator
                    print(
                        f"Password field found: {selector}"
                    )
                    break

            except PlaywrightTimeoutError:
                continue

        if password_field is None:
            raise RuntimeError(
                "Naukri password field was not found."
            )

        password_field.fill(PASSWORD)

        # ====================================================
        # 4. Login
        # ====================================================

        print("4/9 Clicking Login...")

        login_selectors = [
            "button:has-text('Login')",
            "button[type='submit']",
            "input[type='submit']"
        ]

        login_clicked = False

        for selector in login_selectors:
            try:
                button = page.locator(selector).first

                if button.is_visible(timeout=3000):
                    button.click()

                    print(
                        f"Login clicked using: {selector}"
                    )

                    login_clicked = True
                    break

            except PlaywrightTimeoutError:
                continue

        if not login_clicked:
            raise RuntimeError(
                "Naukri Login button was not found."
            )

        page.wait_for_timeout(7000)

        # ====================================================
        # 5. Profile
        # ====================================================

        print("5/9 Navigating to profile...")

        page.goto(
            "https://www.naukri.com/mnjuser/profile",
            wait_until="domcontentloaded",
            timeout=60000
        )

        page.wait_for_timeout(5000)

        print(
            "Profile URL:",
            page.url
        )

        # ====================================================
        # 6. Find upload
        # ====================================================

        print("6/9 Looking for file upload...")

        file_input = page.locator(
            "input[type='file']"
        ).first

        # ====================================================
        # 7. Upload resume
        # ====================================================

        print("7/9 Uploading resume...")

        if file_input.count() > 0:

            file_input.set_input_files(
                RESUME_PATH
            )

            print(
                "Resume uploaded via file input!"
            )

        else:

            raise RuntimeError(
                "Resume file input was not found."
            )

        # ====================================================
        # 8. Wait for upload
        # ====================================================

        print("8/9 Waiting for upload...")

        page.wait_for_timeout(5000)

        # ====================================================
        # 9. Done
        # ====================================================

        print("9/9 Done! Resume upload process completed.")

        browser.close()


if __name__ == "__main__":

    headless = "--headless" in sys.argv

    print("=" * 45)
    print("  Naukri Resume Uploader")
    print(
        f"  Mode: {'CI (headless)' if headless else 'Local'}"
    )
    print("=" * 45)

    login_and_upload(
        headless=headless
    )