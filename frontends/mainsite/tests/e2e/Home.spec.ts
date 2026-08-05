import { test, expect } from '@playwright/test'

test('should display the correct page title and navigation links', async ({ page }) => {
  await page.goto('/')
  
  const pageTitle = await page.title()
  expect(pageTitle).toBe('')

  // Check that the navigation links are present
  await expect(page.getByRole('link', { name: 'Accueil' })).toBeVisible()
  await expect(page.getByRole('link', { name: 'Chansons' })).toBeVisible()
  await expect(page.getByRole('link', { name: 'Statistiques' })).toBeVisible()
  await expect(page.getByRole('link', { name: 'À propos' })).toBeVisible()
  
  // Should be able to toggle dark mode
  await page.locator('#second-header').getByRole('switch').check()
  
  const strHtmlClass = await page.locator('html').getAttribute('class')
  expect(strHtmlClass).toContain('p-dark')

  // Should be able to switch languages
  await page.getByRole('button', { name: 'Passer en français' }).click()

  expect(page.url()).toContain('/')
  await page.getByRole('button', { name: 'Passer en anglais' }).click()

  // When the application first starts, a new session storage
  // item should be created for the blindtestId. It should be
  // found in the session storage of the page.
  const blindtestId = await page.sessionStorage.getItem('blindtestId')
  expect(blindtestId).not.toBeNull()

  // We should be able to start a new blindtest by clicking the start button
  const startLocator = page.getByRole('button', { name: 'Démarrer' })
  await expect(startLocator).toBeVisible()
  await expect(startLocator).toBeEnabled()
  await startLocator.click()

  await page.waitForURL(/\/en\/blindtest\?id=/)
  expect(page.url()).toContain('/en/blindtest')

  const url = new URL(page.url())
  const blindtestIdFromUrl = url.searchParams.get('id')
  expect(blindtestIdFromUrl).toBe(blindtestId)
})

test('should be able to navigate the home page', async ({ page }) => {
  await page.goto('/')

  // Click on the navigation links and check that the page changes accordingly
  await page.getByRole('link', { name: 'Chansons' }).click()
  await page.waitForURL(/\/en\/create-songs/)

  await page.getByRole('link', { name: 'Statistiques' }).click()
  await page.waitForURL(/\/en\/statistics/)

  await page.getByRole('link', { name: 'À propos' }).click()
  await page.waitForURL(/\/en\/about/)

  await page.getByRole('link', { name: 'Accueil' }).click()
  await page.waitForURL('/')
})
