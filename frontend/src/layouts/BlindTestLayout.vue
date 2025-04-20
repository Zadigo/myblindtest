<template>
  <section class="h-auto relative">
    <div class="grid grid-cols-2 grid-rows-1">
      <div id="team-1">
        <slot name="teamOne" />
      </div>

      <div id="team-2">
        <slot name="teamTwo" />
      </div>

      <!-- Video -->
      <slot name="video" />
    </div>

    <slot />
  </section>
</template>
