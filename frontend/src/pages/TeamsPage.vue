<template>
  <section class="w-5xl mx-auto px-10 relative">
    <div class="grid grid-cols-12 gap-2 my-10">
      <div class="col-span-12">
        <Card>
          <CardContent>
            <div class="space-x-2">
              <Button class="ml-auto rounded-full" as-child>
                <RouterLink :to="{ name: 'home' }">
                  Back to settings
                </RouterLink>
              </Button>

              <Button class="rounded-full" as-child>
                <RouterLink :to="{ name: 'blind_test' }">
                  Go to blindtest
                </RouterLink>
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      <div class="col-span-6">
        <Card>
          <CardContent>
            <Input v-model="teamOne.name" placeholder="Team name" />
          </CardContent>
        </Card>
      </div>

      <div class="col-span-6">
        <Card>
          <CardContent>
            <Input v-model="teamTwo.name" placeholder="Team name" />
          </CardContent>
        </Card>
      </div>

      <div class="col-span-12">
        <Card>
          <CardContent class="card-body">
            <div class="flex gap-2">
              <Button :active="selectedTeam===1" @click="selectedTeam=1">
                Team 1
              </Button>

              <Button :active="selectedTeam===2" @click="selectedTeam=2">
                Team 2
              </Button>
            </div>

            <div class="flex justify-center my-10">
              {{ debouncedWheelColor }}
              <VueColorWheel v-model:color="wheelColor" wheel="aurora" harmony="complementary" :radius="160" :default-color="wheelColor" @change="handleChangeColor" />
            </div>

            <Input v-model="wheelColor" />
          </CardContent>
        </Card>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { Harmony } from 'vue-color-wheel'
import { VueColorWheel } from 'vue-color-wheel'

useHead({
  title: 'Settings'
})

const songsStore = useSongs()
// const wheelColor = useDebounce(ref<string>('#5a228b'))
const wheelColor = shallowRef('#5a228b')
const debouncedWheelColor = refDebounced(wheelColor, 1000)

const selectedTeam = ref(1)
const colorList = ref<Harmony[]>()

const teamOne = computed(() => {
  return songsStore.cache.teams[0]
})

const teamTwo = computed(() => {
  return songsStore.cache.teams[1]
})

watch(wheelColor, (newValue) => {
  if (selectedTeam.value === 1) {
    songsStore.cache.teams[0].color = newValue
  } else {
    songsStore.cache.teams[1].color = newValue
  }
})

/**
 * @param harmonyColors Something
 */
function handleChangeColor(harmonyColors: Harmony[]) {
  colorList.value = harmonyColors
}
</script>
