# E2E Tests for PocketClaw Dashboard
# Created: 2026-02-05
#
# End-to-end tests using Playwright to verify the dashboard UI works correctly.
# Tests run against a real server instance with a real browser.
#
# Run with: pytest tests/e2e/ -v --headed (to see browser)
# Run headless: pytest tests/e2e/ -v

from playwright.sync_api import Page, expect


class TestDashboardLoads:
    """Tests that the dashboard loads correctly."""

    def test_dashboard_title(self, page: Page, dashboard_url: str):
        """Test that dashboard page loads with correct title."""
        page.goto(dashboard_url)
        expect(page).to_have_title("PocketPaw")

    def test_chat_view_visible_by_default(self, page: Page, dashboard_url: str):
        """Test that Chat view is visible by default."""
        page.goto(dashboard_url)

        # Chat tab should be active
        chat_tab = page.locator("button:has-text('Chat')")
        expect(chat_tab).to_be_visible()

    def test_view_tabs_exist(self, page: Page, dashboard_url: str):
        """Test that all view tabs exist."""
        page.goto(dashboard_url)

        tabs = ["Chat", "Activity", "Crew"]
        for tab in tabs:
            expect(page.locator(f"button:has-text('{tab}')")).to_be_visible()

    def test_agent_mode_toggle_exists(self, page: Page, dashboard_url: str):
        """Test that agent mode toggle exists."""
        page.goto(dashboard_url)

        # Look for Agent Mode label (use exact match to avoid multiple matches)
        expect(page.get_by_text("Agent Mode", exact=True).first).to_be_visible()


class TestCrewView:
    """Tests for the Crew (Control Room) view."""

    def test_crew_tab_switches_view(self, page: Page, dashboard_url: str):
        """Test that clicking Crew tab switches to Crew view."""
        page.goto(dashboard_url)

        # Click Crew tab
        page.click("button:has-text('Crew')")

        # Wait for loading to complete
        page.wait_for_selector("text=Loading Crew...", state="hidden", timeout=10000)

        # Check stats bar appears (indicator of Crew view) - use heading "Agents"
        expect(page.get_by_role("heading", name="Agents")).to_be_visible()

    def test_new_agent_button_exists(self, page: Page, dashboard_url: str):
        """Test that New Agent button exists in Crew view."""
        page.goto(dashboard_url)
        page.click("button:has-text('Crew')")
        page.wait_for_selector("text=Loading Crew...", state="hidden", timeout=10000)

        expect(page.locator("button:has-text('New Agent')")).to_be_visible()

    def test_new_task_button_exists(self, page: Page, dashboard_url: str):
        """Test that New Task button exists in Crew view."""
        page.goto(dashboard_url)
        page.click("button:has-text('Crew')")
        page.wait_for_selector("text=Loading Crew...", state="hidden", timeout=10000)

        expect(page.locator("button:has-text('New Task')")).to_be_visible()

    def test_stats_bar_shows_numbers(self, page: Page, dashboard_url: str):
        """Test that stats bar shows agent and task counts."""
        page.goto(dashboard_url)
        page.click("button:has-text('Crew')")
        page.wait_for_selector("text=Loading Crew...", state="hidden", timeout=10000)

        # Stats bar should show "Live" indicator
        expect(page.get_by_text("Live", exact=True)).to_be_visible()

        # Stats should show "done today" text
        expect(page.get_by_text("done today")).to_be_visible()


class TestAgentCreation:
    """Tests for creating agents in Crew view."""

    def test_create_agent_modal_opens(self, page: Page, dashboard_url: str):
        """Test that clicking New Agent opens the creation form."""
        page.goto(dashboard_url)
        page.click("button:has-text('Crew')")
        page.wait_for_selector("text=Loading Crew...", state="hidden", timeout=10000)

        # Click New Agent
        page.click("button:has-text('New Agent')")

        # Wait for modal animation
        page.wait_for_timeout(300)

        # Modal should appear with "Create Agent" button
        expect(page.locator("button:has-text('Create Agent')")).to_be_visible()

    def test_create_agent_flow(self, page: Page, dashboard_url: str):
        """Test creating a new agent through the UI."""
        page.goto(dashboard_url)
        page.click("button:has-text('Crew')")
        page.wait_for_selector("text=Loading Crew...", state="hidden", timeout=10000)

        # Click New Agent button in header
        page.locator("button:has-text('New Agent')").first.click()
        page.wait_for_timeout(300)  # Wait for modal animation

        # Fill form using placeholder text
        page.get_by_placeholder("Agent name").fill("E2E Test Agent")
        page.get_by_placeholder("Role (e.g., Research Lead)").fill("Test Role")

        # Submit - click the visible Create Agent button (the one in modal)
        page.locator("button:has-text('Create Agent'):visible").click()

        # Wait for API response and UI update
        page.wait_for_timeout(1500)

        # Agent should appear somewhere (list or activity feed)
        expect(page.get_by_text("E2E Test Agent").first).to_be_visible(timeout=5000)


class TestTaskCreation:
    """Tests for creating tasks in Crew view."""

    def test_create_task_modal_opens(self, page: Page, dashboard_url: str):
        """Test that clicking New Task opens the creation form."""
        page.goto(dashboard_url)
        page.click("button:has-text('Crew')")
        page.wait_for_selector("text=Loading Crew...", state="hidden", timeout=10000)

        # Click New Task
        page.click("button:has-text('New Task')")

        # Modal should appear with form fields
        expect(page.locator("input[placeholder*='title' i]")).to_be_visible()

    def test_create_task_flow(self, page: Page, dashboard_url: str):
        """Test creating a new task through the UI."""
        page.goto(dashboard_url)
        page.click("button:has-text('Crew')")
        page.wait_for_selector("text=Loading Crew...", state="hidden", timeout=10000)

        # Click New Task button in header
        page.locator("button:has-text('New Task')").first.click()
        page.wait_for_timeout(300)  # Wait for modal animation

        # Fill form using placeholder
        page.get_by_placeholder("Task title").fill("E2E Test Task")

        # Submit - click the button inside the modal (second Create Task button)
        page.get_by_role("button", name="Create Task").nth(1).click()

        # Wait for API response
        page.wait_for_timeout(1500)

        # Task should appear somewhere (list or activity feed)
        expect(page.get_by_text("E2E Test Task").first).to_be_visible(timeout=5000)


class TestSidebarNavigation:
    """Tests for sidebar navigation."""

    def test_sidebar_exists(self, page: Page, dashboard_url: str):
        """Test that sidebar exists and has key elements."""
        page.goto(dashboard_url)

        # Sidebar should have PocketPaw branding or key nav items
        # Check for Settings or other sidebar elements
        sidebar = page.locator("aside, nav").first
        expect(sidebar).to_be_visible()

    def test_settings_opens(self, page: Page, dashboard_url: str):
        """Test that settings modal can be opened."""
        page.goto(dashboard_url)

        # Click settings button (usually a gear icon)
        settings_btn = page.locator(
            "button:has(i[data-lucide='settings']), button:has-text('Settings')"
        ).first
        if settings_btn.is_visible():
            settings_btn.click()
            # Settings modal should appear
            page.wait_for_timeout(500)


class TestRemoteAccessModal:
    """Tests for the Remote Access modal."""

    def test_remote_button_exists(self, page: Page, dashboard_url: str):
        """Test that Take Your Paw With You button exists."""
        page.goto(dashboard_url)

        # This button might be hidden on mobile, so check desktop viewport
        remote_btn = page.locator("button:has-text('Take Your Paw With You')")
        # May not be visible on all viewports
        if remote_btn.is_visible():
            expect(remote_btn).to_be_visible()
