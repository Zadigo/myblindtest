import { test, expect } from '@playwright/test'

test('visits the app root url', async ({ page }) => {
  await page.goto('/create-songs')

  const titleEl = page.getByText('Create songs')
  expect(titleEl).toBeVisible()
})
