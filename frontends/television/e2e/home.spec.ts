import { test, expect } from '@playwright/test'

test('visits the app root url', async ({ page }) => {
  await page.goto('/')

  const title = page.locator('h1')
  await expect(title).toHaveText('Blind test')
  
  const inputEl = page.getByRole('textbox', { disabled: false })
  await expect(inputEl).toBeVisible()
  await expect(inputEl.getAttribute('disabled')).toBeDefined()

  const buttonEl = page.locator('#action-connect')
  await expect(buttonEl).toBeDefined()
})
