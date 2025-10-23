<template>
  <div class="my-10 flex-col justify-center space-y-5">
    <div class="flex justify-around gap-2">
      <VoltContrastButton class="w-full">
        <vue-icon icon="lucide:star-half" />
        Title
      </VoltContrastButton>
      <VoltContrastButton class="w-full">
        <vue-icon icon="lucide:star-half" />
        Artist
      </VoltContrastButton>
      <VoltContrastButton class="w-full">
        <vue-icon icon="lucide:star" />
        Both
      </VoltContrastButton>
    </div>
    
    <VoltContrastButton class="w-full">
      <vue-icon icon="lucide:check" />
      Validate
    </VoltContrastButton>
  </div>
</template>
