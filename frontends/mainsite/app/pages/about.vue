<template>
  <volt-container class="h-screen" size="md">
    <div class="grid grid-cols-3 gap-2 grid-flow-row-dense">
      <div class="p-10 rounded-xl bg-primary-100 col-span-3 dark:bg-primary-800 dark:text-surface-50">
        <h1 class="font-bold text-4xl mb-4">
          About MyBlindTest
        </h1>

        <p class="font-light">
          MyBlindTest is a platform that allows users to create and participate in blind tests, helping
          them improve their skills and knowledge in various subjects.

          The platform is built using modern web technologies, including Vue.js for the frontend and Django
          for the backend. It offers a user-friendly interface and a variety of features to enhance the
          blind test experience.
        </p>
      </div>

      <div class="p-10 rounded-xl bg-primary-100 col-span-2 dark:bg-primary-800 dark:text-surface-50">
        <h3 class="font-bold text-2xl">Point system</h3>
        Lorem ipsum dolor sit amet consectetur, adipisicing elit. Consequuntur placeat aliquid vitae obcaecati quo quisquam aspernatur, ullam, sequi laborum tenetur esse alias cum harum inventore id reiciendis quae? Accusamus, voluptates?
      </div>

      <div class="p-10 rounded-xl bg-primary-100 col-span-3 dark:bg-primary-800 dark:text-surface-50">
        <h3 class="font-bold text-2xl">Point system</h3>
        Lorem ipsum dolor sit amet consectetur, adipisicing elit. Consequuntur placeat aliquid vitae
      </div>

      <div class="p-10 rounded-xl bg-primary-100 col-span-2 dark:bg-primary-800 dark:text-surface-50">
        <h3 class="font-bold text-2xl">Point system</h3>
        Lorem ipsum dolor sit amet consectetur, adipisicing elit. Consequuntur placeat aliquid vitae obcaecati quo quisquam aspernatur, ullam, sequi laborum tenetur esse alias cum harum inventore id reiciendis quae? Accusamus, voluptates?
      </div>

      <div class="p-10 rounded-xl bg-primary-100 col-span-1 dark:bg-primary-800 dark:text-surface-50">
        <h3 class="font-bold text-2xl">Point system</h3>
        Lorem ipsum dolor sit amet consectetur, adipisicing elit. Consequuntur placeat aliquid vitae
      </div>

      <div class="p-10 rounded-xl bg-primary-100 col-span-1 dark:bg-primary-800 dark:text-surface-50">
        <h3 class="font-bold text-2xl">Point system</h3>
        Lorem ipsum dolor sit amet consectetur, adipisicing elit. Consequuntur placeat aliquid vitae
      </div>
    </div>
  </volt-container>
</template>

<script lang="ts" setup>
/**
 * SEO
 */

const { locale } = useI18n()

const titles = {
  en: 'About MyBlindTest',
  fr: 'À propos de MyBlindTest',
}

const descriptions = {
  'en': 'Join the ultimate blind test challenge! Test your music knowledge with friends and climb the leaderboard. Are you ready to take on the challenge?',
  'fr': "Rejoignez le défi blindtest ultime ! Testez vos connaissances musicales avec des amis et grimpez dans le classement. Êtes-vous prêt à relever le défi ?",
}

useHead({
  title: titles[locale.value],
  meta: [
    {
      name: 'description',
      content: descriptions[locale.value],
    },
  ],
})
</script>
