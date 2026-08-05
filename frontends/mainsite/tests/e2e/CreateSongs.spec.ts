import { test, expect } from '@playwright/test'

test('should contain all the required elements', async ({ page }) => {
  await page.goto('/create-songs')

  // The components changes based on the flag in the url query
  const url = new URL(page.url())
  expect(url.searchParams.get('v')).toEqual('c')


  // const titleEl = page.getByText('Create songs')
  // expect(titleEl).toBeVisible()
})

test('should be able to create a song', async ({ page }) => {
  await page.goto('/create-songs')

  await page.getByRole('textbox', { name: 'Nom de la chanson' }).click()
  await page.getByRole('textbox', { name: 'Nom de la chanson' }).fill('Test Song')
  await page.getByRole('button').first().click()
  
  await page.getByRole('option', { name: 'African heavy metal' }).click()

  await page.getByRole('spinbutton', { name: 'Difficulté' }).click()
  await page.getByRole('button').nth(1).click()
  
  await page.getByRole('option', { name: '1T1' }).click()


  await page.getByRole('option', { name: '1T1' }).click();

  await page.getByRole('textbox', { name: 'Hzu-GygG6zs, https://www.' }).click()
  await page.getByRole('textbox', { name: 'Hzu-GygG6zs, https://www.' }).fill('dNt1QR1ecuM')
})

test('should be able to get all the songs created', async ({ page }) => {
  await page.goto('/create-songs')

  await page.getByRole('button', { name: 'Chansons' }).click()

  // Search for the artist and select it
  const searchLocator = page.getByRole('searchbox', { name: 'Rechercher des artistes, des' })
  await searchLocator.waitFor({ state: 'visible' })

  await searchLocator.click()
  await searchLocator.fill('mariah carey')

  // const url = new URL(page.url())
  // expect(url.searchParams.get('q')).toEqual('mariah carey')

  const artistButton = page.getByRole('button', { name: 'Mariah Carey 15 songs' })
  await artistButton.waitFor({ state: 'visible' })
  await artistButton.click()

  const wikiLocator = page.getByRole('link', { name: 'Page Wikipedia' })
  expect(wikiLocator).toBeVisible()
  expect(wikiLocator).toBeEnabled()
})
