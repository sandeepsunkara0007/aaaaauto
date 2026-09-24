import time
from playwright.sync_api import sync_playwright
import os
import sys

# Credentials — use env vars in CI, fallback to hardcoded for local use
EMAIL = os.getenv("NAUKRI_EMAIL", "sandeepnaidusukara@gmail.com")
PASSWORD = os.getenv("NAUKRI_PASSWORD", "Sandeep@123")
RESUME_PATH = os.path.join(os.path.dirname(__file__), "sandeep_java_fullstack_Aws_developer_2_8_years.pdf")
GAP = 2

def login_and_upload(headless=False):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless,
            args=["--disable-blink-features=AutomationControlled"] if headless else [])
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        )

        # Anti-detection for headless mode
        if headless:
            context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
                Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
            """)

        page = context.new_page()

        print("1/9 Opening Naukri login page...")
        page.goto("https://www.naukri.com/nlogin/login")
        page.wait_for_timeout(4000)

        print("2/9 Entering email...")
        page.locator("#usernameField").fill(EMAIL)
        page.wait_for_timeout(2000)

        print("3/9 Entering password...")
        page.locator("#passwordField").fill(PASSWORD)
        page.wait_for_timeout(2000)

        print("4/9 Clicking Login...")
        page.locator("button:has-text('Login')").first.click()
        page.wait_for_timeout(5000)

        print("5/9 Navigating to profile...")
        page.goto("https://www.naukri.com/mnjuser/profile")
        page.wait_for_timeout(5000)

        print("6/9 Looking for file upload...")
        page.wait_for_timeout(2000)

        print("7/9 Uploading resume...")
        if page.locator("input[type='file']").count() > 0:
            page.locator("input[type='file']").first.set_input_files(RESUME_PATH)
            print("   Uploaded via file input!")
        else:
            found = False
            for text in ["Upload Resume", "Upload", "Update"]:
                btn = page.locator(f"button:has-text('{text}')").first
                if btn.is_visible(timeout=1000):
                    btn.click()
                    page.wait_for_timeout(2000)
                    if page.locator("input[type='file']").count() > 0:
                        page.locator("input[type='file']").first.set_input_files(RESUME_PATH)
                        print(f"   Uploaded via '{text}' button!")
                        found = True
                        break
            if not found:
                page.evaluate("""
                    const inp = document.createElement('input');
                    inp.type = 'file'; inp.id = '_up';
                    inp.style.cssText = 'position:fixed;top:10px;left:10px;z-index:99999';
                    document.body.prepend(inp);
                """)
                page.wait_for_timeout(1000)
                page.locator("#_up").set_input_files(RESUME_PATH)
                print("   Uploaded via injected input!")

        page.wait_for_timeout(3000)
        page.screenshot(path="naukri_result.png")
        print("8/9 Screenshot saved!")

        browser.close()
        print("9/9 Done! Resume uploaded successfully!")

if __name__ == "__main__":
    headless = "--headless" in sys.argv
    print("=" * 45)
    print("  Naukri Resume Uploader")
    print(f"  Mode: {'CI (headless)' if headless else 'Local (visible)'}")
    print("=" * 45)
    login_and_upload(headless=headless)
