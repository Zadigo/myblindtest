<template>
  <div id="dock" ref="dockEl" class="col-span-12 bg-primary-100/30 border border-primary-100/20 backdrop-blur-xl shadow-md dark:bg-primary-950 dark:border-none dark:shadow-2xl h-auto min-w-100 w-150 absolute bottom-10 left-[calc(50%-calc(600px/2))] px-2 py-3 rounded-xl flex justify-center gap-2 z-40 overflow-hidden">
    <transition-group enter-from-class="animate-fadeinup" enter-to-class="animate-fadeindown" leave-from-class="animate-fadeindown" leave-to-class="animate-fadeinup">
      <volt-button v-for="item in items" :key="item.icon" :disabled="item.name === 'Pause'" @click="item.action">
        <icon :name="item.icon" class="text-xl" />
      </volt-button>
    </transition-group>

    <sound-effect v-if="currentSettings && !currentSettings.settings.multipleChoiceAnswers" id="sound-wrong-answer" name="cinematic-hit">
      <template #default="{ attrs }">
        <volt-secondary-button @click="attrs.playSound(sendIncorrectAnswer)">
          <icon name="lucide:x-square" class="text-xl" />
          {{ $t('Wrong Answer') }}
        </volt-secondary-button>
      </template>
    </sound-effect>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'

/**
 * Ranadomizer
 */

const { showWheel } = useWheelRandomizer()

/**
 * Websocket
 */

const { wsObject, gameStarted } = useAdminWebsocket()
const { startGame, pauseGame, sendIncorrectAnswer } = useGameActions(wsObject, gameStarted)

/**
 * Timer
 */

const { restart, hasTimer } = useGameCountdown()

/**
 * Dock Buttons
 */

const { t } = useI18n()

const baseDockItems = [
  {
    name: t('Play'),
    icon: 'lucide:play',
    action: startGame
  },
  {
    name: t('Pause'),
    icon: 'lucide:pause',
    action: () => pauseGame()
  },
  {
    name: t('Randomizer'),
    icon: 'lucide:zap',
    action: () => { showWheel.value = !showWheel.value }
  }
]

const baseActionDockItems = computed(() => {
  const baseItems = [...baseDockItems]

  if (hasTimer.value) {
    baseItems.splice(1, 0, {
      name: t('Restart Timer'),
      icon: 'lucide:timer-reset',
      action: restart
    })
  }

  return baseItems
})

const { updateAnswersWithCountdown } = useMultiChoiceGameActions(wsObject)

const multiChoiceActionDockItems = computed(() => {
  const baseItems = [
    ...baseDockItems,
    {
      name: t('Show Scores'),
      icon: 'lucide:chevron-right',
      action: () => updateAnswersWithCountdown()
    }
  ]

  return baseItems
})

const { currentSettings } = useSession()

const items = computedAsync(() => {
  if (isDefined(currentSettings)) {
    if (currentSettings.value.settings.multipleChoiceAnswers) {
      return multiChoiceActionDockItems.value
    } else {
      return baseActionDockItems.value
    }
  }
})
</script>
