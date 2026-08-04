import { test, expect } from '@playwright/test'

test('visits the about page', async ({ page }) => {
  await page.goto('/about')

  const titleEl = page.getByText('About MyBlindTest')
  expect(titleEl).toBeVisible()
})
