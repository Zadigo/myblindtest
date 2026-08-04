import { test, expect } from '@playwright/test'

test('visits the app root url', async ({ page }) => {
  await page.goto('/')
  
  const pageTitle = await page.title()
  expect(pageTitle).toBe('')
})
