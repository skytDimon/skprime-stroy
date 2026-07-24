<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const currentYear = new Date().getFullYear()

/* ───── mobile nav ───── */
const mobileMenuOpen = ref(false)
const toggleMenu = () => { mobileMenuOpen.value = !mobileMenuOpen.value }

/* ───── header scroll shadow ───── */
const scrolled = ref(false)
function onScroll() { scrolled.value = window.scrollY > 20 }
onMounted(() => window.addEventListener('scroll', onScroll))
onUnmounted(() => window.removeEventListener('scroll', onScroll))

/* ───── smooth scroll ───── */
function scrollTo(id) {
  mobileMenuOpen.value = false
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' })
}
function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

/* ───── contact form ───── */
const form = ref({ name: '', phone: '', objectType: '', otherDetails: '' })
const sending = ref(false)
const sent = ref(false)
const error = ref('')

const selectedService = ref(null)

function closeModalAndScrollToContact() {
  if (selectedService.value) {
    form.value.objectType = 'special_works'
    form.value.otherDetails = selectedService.value.title
  }
  selectedService.value = null
  setTimeout(() => {
    scrollTo('contact')
  }, 100)
}

async function submitForm() {
  error.value = ''
  if (!form.value.name || !form.value.phone || !form.value.objectType) {
    error.value = 'Заполните все поля формы.'
    return
  }
  sending.value = true
  try {
    const res = await fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form.value)
    })
    if (!res.ok) throw new Error('Ошибка сервера')
    sent.value = true
    form.value = { name: '', phone: '', objectType: '' }
  } catch (e) {
    error.value = 'Не удалось отправить заявку. Попробуйте позже.'
  } finally {
    sending.value = false
  }
}

/* ───── services data ───── */
const services = [
  {
    title: 'Промышленные и административные здания',
    desc: 'Полный цикл строительства объектов промышленного и административного назначения — от нулевого цикла до сдачи под ключ.',
    detailedDesc: 'Мы выполняем полный цикл строительства промышленных и административных объектов. Наши компетенции охватывают земляные работы, возведение фундамента, монтаж каркаса здания, ограждающих конструкций и кровли, а также финишную отделку и благоустройство территории.',
    images: ['11.png'],
    icon: 'M3 21h18M3 7v1a3 3 0 006 0V7m0 1a3 3 0 006 0V7m0 1a3 3 0 006 0V7H3l2-4h14l2 4M5 21V10.7M19 21V10.7'
  },
  {
    title: 'Фундаменты',
    desc: 'Устройство монолитных, свайных и плитных фундаментов на основании результатов инженерно-геологических изысканий.',
    detailedDesc: 'Качественный фундамент — основа любого промышленного сооружения. Выполняем устройство свайных, ленточных и монолитных плитных фундаментов высокой сложности с учетом геологии участка и расчетных нагрузок.',
    images: ['22.png'],
    icon: 'M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0H5m14 0h2m-16 0H3m2-7h4m-4 4h4m6-4h4m-4 4h4'
  },
  {
    title: 'Металлоконструкции и ж/б каркасы',
    desc: 'Изготовление и монтаж металлических конструкций по КМД, сборка железобетонных каркасов.',
    detailedDesc: 'Производим сборку и надежный монтаж металлических и железобетонных конструкций. Сварочные и монтажные работы проводятся исключительно аттестованными специалистами НАКС с обязательным инструментальным и визуальным контролем (УЗК/ВИК).',
    images: ['33.png', '34.png'],
    icon: 'M4 6h16M4 10h16M4 14h16M4 18h16'
  },
  {
    title: 'Промышленные полы',
    desc: 'Устройство бетонных, полимерных и топпинговых промышленных полов с нагрузочной способностью до 10 т/м².',
    detailedDesc: 'Создаем высокопрочные промышленные полы: бетонные с упрочненным верхним слоем (топпинг), полимерные, эпоксидные и полиуретановые покрытия. Они устойчивы к химическим и механическим воздействиям, не пылят и выдерживают огромные нагрузки оборудования и техники.',
    images: ['44.png'],
    icon: 'M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2'
  },
  {
    title: 'Инженерные сети',
    desc: 'Проектирование и монтаж наружных и внутренних инженерных сетей: водоснабжение, канализация, отопление, вентиляция, электроснабжение.',
    detailedDesc: 'Выполняем полный комплекс работ по устройству внутренних и наружных инженерных коммуникаций (электроснабжение, водопровод, отопление, вентиляция и канализация). Пусконаладочные работы и сдача надзорным органам производятся под ключ.',
    images: ['55.png'],
    icon: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065zM15 12a3 3 0 11-6 0 3 3 0 016 0z'
  }
]
</script>

<template>
  <div class="relative min-h-screen text-neutral-900 antialiased" style="font-family: 'Inter', system-ui, sans-serif;">
    <!-- background image -->
    <div class="fixed inset-0 z-0 pointer-events-none" style="background: url('/background.png') center / cover no-repeat fixed;"></div>

    <!-- ══════════ HEADER ══════════ -->
    <header
      :class="[
        'fixed top-0 left-0 right-0 z-50 transition-all duration-300',
        scrolled
          ? 'bg-white/95 backdrop-blur-xl shadow-2xl shadow-black/8'
          : 'bg-transparent'
      ]"
    >
      <div class="max-w-[1400px] mx-auto px-6 lg:px-10">
        <div class="flex items-center justify-between h-20 lg:h-28">

          <!-- logo -->
          <button @click="scrollToTop" class="flex items-end gap-4 shrink-0 cursor-pointer text-left">
            <img src="/logo.png" alt="ПРАЙМ-СТРОЙ" class="w-20 h-20 lg:w-24 lg:h-24 rounded-2xl object-contain" />
            <div class="hidden md:block mb-7 lg:mb-7">
              <span class="block text-xs lg:text-sm tracking-[0.2em] uppercase text-neutral-400">строительная компания</span>
            </div>
          </button>

          <!-- desktop nav -->
          <nav class="hidden lg:flex items-center gap-10 text-lg font-semibold text-neutral-600">
            <button @click="scrollTo('about')" class="hover:text-teal-600 transition-colors cursor-pointer">О компании</button>
            <button @click="scrollTo('services')" class="hover:text-teal-600 transition-colors cursor-pointer">Услуги</button>
            <button @click="scrollTo('contact')" class="hover:text-teal-600 transition-colors cursor-pointer">Контакты</button>
          </nav>

          <!-- phone + burger -->
          <div class="flex items-center gap-5">
            <a href="tel:+79222011801"
               class="hidden md:flex items-center gap-3 text-lg font-bold text-teal-600 hover:text-teal-500 transition-colors">
              <div class="w-12 h-12 rounded-xl flex items-center justify-center bg-teal-50">
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
              </div>
              +7 (922) 201-18-01
            </a>

            <button @click="toggleMenu" class="lg:hidden cursor-pointer p-2 -mr-2 text-neutral-600 hover:text-neutral-900">
              <svg class="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16"/>
                <path v-else stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- mobile menu -->
      <transition
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="opacity-0 -translate-y-2"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition duration-150 ease-in"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 -translate-y-2"
      >
        <div v-if="mobileMenuOpen" class="lg:hidden bg-white/98 backdrop-blur-xl border-t border-neutral-200">
          <div class="px-6 py-6 flex flex-col gap-1">
            <button @click="scrollTo('about')" class="text-left text-lg font-semibold py-3 cursor-pointer text-neutral-600 hover:text-teal-600 transition-colors">О компании</button>
            <button @click="scrollTo('services')" class="text-left text-lg font-semibold py-3 cursor-pointer text-neutral-600 hover:text-teal-600 transition-colors">Услуги</button>
            <button @click="scrollTo('contact')" class="text-left text-lg font-semibold py-3 cursor-pointer text-neutral-600 hover:text-teal-600 transition-colors">Контакты</button>
            <a href="tel:+79222011801" class="text-lg font-bold py-3 text-teal-600">+7 (922) 201-18-01</a>
          </div>
        </div>
      </transition>
    </header>


    <!-- ══════════ HERO ══════════ -->
    <section class="relative z-[1] min-h-screen flex items-center overflow-hidden">

      <div class="relative max-w-[1400px] mx-auto px-6 lg:px-10 py-36 lg:py-44">
        <div class="max-w-4xl">
          <div class="inline-flex items-center gap-3 px-5 py-2 rounded-full text-sm font-semibold mb-10 bg-teal-50 border border-teal-200 text-teal-700">
            <span class="w-2.5 h-2.5 rounded-full bg-teal-500 animate-pulse"></span>
            Екатеринбург и Свердловская область
          </div>

          <h1 class="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-black leading-[1.1] tracking-tight text-neutral-900">
            Строим промышленные<br/>объекты
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-teal-600 to-cyan-600"> точно в&nbsp;срок</span>
          </h1>

          <p class="mt-8 lg:mt-10 text-lg lg:text-xl leading-relaxed max-w-2xl text-neutral-500">
            ООО&nbsp;СК&nbsp;«ПРАЙМ&#8209;СТРОЙ» — генеральный подрядчик полного цикла. Фундаменты, металлоконструкции, ж/б&nbsp;каркасы, промышленные полы и&nbsp;инженерные сети. Все работы — с&nbsp;допуском&nbsp;СРО, по&nbsp;ГОСТ и&nbsp;СП, с&nbsp;фиксированным графиком производства работ.
          </p>

          <div class="mt-10 lg:mt-12 flex flex-wrap gap-5">
            <button
              @click="scrollTo('contact')"
              class="px-10 py-5 text-lg font-bold rounded-2xl bg-gradient-to-r from-teal-600 to-cyan-600 text-white shadow-xl shadow-teal-600/25 hover:shadow-teal-600/40 hover:-translate-y-1 transition-all duration-300 cursor-pointer"
            >
              Оставить заявку
            </button>
            <button
              @click="scrollTo('services')"
              class="px-10 py-5 text-lg font-bold rounded-2xl border-2 border-neutral-300 text-neutral-600 hover:border-teal-400 hover:text-teal-600 transition-all duration-300 cursor-pointer"
            >
              Наши компетенции
            </button>
          </div>

          <!-- stats -->
          <div class="mt-16 lg:mt-20 grid grid-cols-3 gap-8 lg:gap-12 max-w-xl">
            <div>
              <div class="text-4xl lg:text-5xl font-black text-neutral-900">8+</div>
              <div class="text-sm lg:text-base mt-2 text-neutral-400">лет на рынке</div>
            </div>
            <div>
              <div class="text-4xl lg:text-5xl font-black text-neutral-900">50+</div>
              <div class="text-sm lg:text-base mt-2 text-neutral-400">объектов сдано</div>
            </div>
            <div>
              <div class="text-4xl lg:text-5xl font-black text-neutral-900">0</div>
              <div class="text-sm lg:text-base mt-2 text-neutral-400">нарушений ТБ</div>
            </div>
          </div>
        </div>
      </div>

      <!-- decorative line -->
      <div class="absolute right-16 top-0 bottom-0 w-px bg-gradient-to-b from-transparent via-teal-300/30 to-transparent hidden xl:block"></div>
    </section>


    <!-- ══════════ ABOUT ══════════ -->
    <section id="about" class="relative z-[1] py-24 lg:py-32">
      <div class="max-w-[1400px] mx-auto px-6 lg:px-10">
        <div class="grid lg:grid-cols-2 gap-16 lg:gap-20 items-center">
          <div>
            <span class="text-sm lg:text-base font-bold tracking-[0.2em] uppercase text-teal-600">О компании</span>
            <h2 class="mt-4 text-3xl sm:text-4xl lg:text-5xl font-black tracking-tight leading-tight text-neutral-900">
              Надёжный <span class="text-transparent bg-clip-text bg-gradient-to-r from-teal-600 to-cyan-600">генеральный подрядчик</span><br class="hidden lg:block"/>
              для промышленного строительства <span class="relative whitespace-nowrap"><span class="relative z-10">под&nbsp;ключ</span><span class="absolute bottom-1 lg:bottom-2 left-0 right-0 h-3 lg:h-4 bg-teal-300/60 -rotate-2 rounded-sm"></span></span>
            </h2>
            <p class="mt-8 text-lg leading-relaxed text-neutral-500">
              ООО&nbsp;СК&nbsp;«ПРАЙМ&#8209;СТРОЙ» специализируется на&nbsp;строительстве промышленных и&nbsp;административных объектов в&nbsp;Свердловской области. Мы&nbsp;работаем как генеральный подрядчик полного цикла: от&nbsp;подготовки площадки до&nbsp;сдачи объекта в&nbsp;эксплуатацию.
            </p>
            <p class="mt-5 text-lg leading-relaxed text-neutral-500">
              Все строительно-монтажные работы ведутся с&nbsp;допуском СРО, в&nbsp;строгом соответствии с&nbsp;ГОСТ, СП&nbsp;и&nbsp;проектной документацией. На&nbsp;каждом объекте действует система производственного контроля и&nbsp;охраны труда.
            </p>
          </div>

          <div class="grid grid-cols-2 gap-5 lg:gap-6">
            <div v-for="item in [
              { label: 'СРО', sub: 'Допуск к генподрядным работам' },
              { label: 'ГОСТ', sub: 'Соответствие стандартам' },
              { label: 'ИД', sub: 'Исполнительная документация' },
              { label: 'ЭДО', sub: 'Контур.Диадок' }
            ]" :key="item.label"
              class="bg-neutral-50 border-2 border-neutral-200 rounded-3xl p-6 lg:p-8 transition-all duration-300 hover:border-teal-300">
              <div class="text-3xl lg:text-4xl font-black text-teal-600 mb-3">{{ item.label }}</div>
              <div class="text-sm lg:text-base text-neutral-500">{{ item.sub }}</div>
            </div>
          </div>
        </div>
      </div>
    </section>


    <!-- ══════════ SERVICES ══════════ -->
    <section id="services" class="relative z-[1] py-24 lg:py-32">
      <div class="max-w-[1400px] mx-auto px-6 lg:px-10">
        <div class="text-center mb-16 lg:mb-20">
          <span class="text-sm lg:text-base font-bold tracking-[0.2em] uppercase text-teal-600">Компетенции</span>
          <h2 class="mt-4 text-3xl sm:text-4xl lg:text-5xl font-black tracking-tight text-neutral-900">
            Комплексные решения<br class="hidden sm:block"/> для&nbsp;вашего объекта
          </h2>
          <p class="mt-6 max-w-3xl mx-auto text-lg text-neutral-500">
            Выполняем весь спектр строительно-монтажных работ собственными аттестованными бригадами. Каждый этап — под контролем ИТР и с оформлением исполнительной документации.
          </p>
        </div>

        <div class="grid md:grid-cols-2 xl:grid-cols-3 gap-6 lg:gap-8">
          <div
            v-for="(s, i) in services"
            :key="i"
            @click="selectedService = s"
            class="group relative bg-white border-2 border-neutral-200 rounded-3xl overflow-hidden p-8 lg:p-10 shadow-lg hover:shadow-teal-900/10 hover:border-teal-400/60 hover:-translate-y-2 transition-all duration-300 cursor-pointer"
          >
            <!-- background image -->
            <div class="absolute inset-0 z-0 opacity-50 bg-cover bg-top transition-transform duration-700 group-hover:scale-105 group-hover:opacity-60" :style="{ backgroundImage: `url('/${i + 1}.png')` }"></div>

            <div class="relative z-10 mt-32 lg:mt-48">
              <h3 class="text-xl lg:text-2xl font-bold text-neutral-900 mb-4">{{ s.title }}</h3>
              <p class="text-base lg:text-lg leading-relaxed font-medium text-neutral-800">{{ s.desc }}</p>
            </div>

            <!-- bottom accent -->
            <div class="absolute bottom-0 left-10 right-10 h-1 rounded-t-full bg-gradient-to-r from-transparent via-teal-400/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 z-10"></div>
          </div>
        </div>
      </div>
    </section>


    <!-- ══════════ CONTACT FORM ══════════ -->
    <section id="contact" class="relative z-[1] py-24 lg:py-32">
      <!-- bg glow -->
      <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_bottom_left,_var(--tw-gradient-stops))] from-teal-100/50 via-transparent to-transparent"></div>

      <div class="relative max-w-[1400px] mx-auto px-6 lg:px-10">
        <div class="grid lg:grid-cols-2 gap-16 lg:gap-20">
          <!-- left: info -->
          <div>
            <span class="text-sm lg:text-base font-bold tracking-[0.2em] uppercase text-teal-600">Связаться с нами</span>
            <h2 class="mt-4 text-3xl sm:text-4xl lg:text-5xl font-black tracking-tight text-neutral-900">Обсудим ваш проект</h2>
            <p class="mt-8 text-lg leading-relaxed text-neutral-500">
              Отправьте заявку — ответим в&nbsp;течение одного рабочего дня. Подготовим коммерческое предложение с&nbsp;фиксированной сметой и&nbsp;графиком работ.
            </p>

            <div class="mt-10 lg:mt-12 space-y-6 lg:space-y-8">
              <div class="flex items-start gap-5">
                <div class="w-14 h-14 rounded-2xl bg-neutral-100 text-teal-600 flex items-center justify-center shrink-0">
                  <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                </div>
                <div>
                  <div class="font-bold text-lg text-neutral-900">Адрес</div>
                  <div class="text-base mt-1 text-neutral-500">г.&nbsp;Екатеринбург, ул.&nbsp;Барвинка,&nbsp;21, офис&nbsp;35</div>
                </div>
              </div>

              <div class="flex items-start gap-5">
                <div class="w-14 h-14 rounded-2xl bg-neutral-100 text-teal-600 flex items-center justify-center shrink-0">
                  <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
                </div>
                <div>
                  <div class="font-bold text-lg text-neutral-900">Email</div>
                  <a href="mailto:office.prime-stroy@ya.ru" class="text-base text-teal-600 hover:text-teal-500 transition-colors">office.prime-stroy@ya.ru</a>
                </div>
              </div>

              <div class="flex items-start gap-5">
                <div class="w-14 h-14 rounded-2xl bg-neutral-100 text-teal-600 flex items-center justify-center shrink-0">
                  <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
                </div>
                <div>
                  <div class="font-bold text-lg text-neutral-900">Телефон</div>
                  <a href="tel:+79222011801" class="text-base text-teal-600 hover:text-teal-500 transition-colors">+7 (922) 201-18-01</a>
                </div>
              </div>
            </div>
          </div>

          <!-- right: form -->
          <div class="bg-white border-2 border-neutral-200 rounded-3xl p-8 lg:p-10 shadow-xl shadow-neutral-200/50">

            <!-- success state -->
            <div v-if="sent" class="text-center py-16">
              <div class="w-20 h-20 rounded-full mx-auto bg-teal-50 text-teal-600 flex items-center justify-center mb-6">
                <svg class="w-10 h-10" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/>
                </svg>
              </div>
              <h3 class="text-2xl font-bold text-neutral-900 mb-3">Заявка отправлена</h3>
              <p class="text-lg text-neutral-500">Мы свяжемся с вами в течение одного рабочего дня.</p>
              <button
                @click="sent = false"
                class="mt-8 px-8 py-3 text-base font-semibold rounded-xl border-2 border-neutral-300 text-neutral-600 hover:border-teal-400 hover:text-teal-600 transition-all cursor-pointer"
              >
                Отправить ещё одну
              </button>
            </div>

            <!-- form -->
            <form v-else @submit.prevent="submitForm" class="space-y-6">
              <div>
                <label for="name" class="block text-base font-semibold text-neutral-700 mb-2">Имя / Компания</label>
                <input
                  id="name"
                  v-model="form.name"
                  type="text"
                  placeholder="Иван Петров, ООО «Заказчик»"
                  class="w-full px-5 py-4 text-base bg-neutral-50 border-2 border-neutral-200 text-neutral-900 placeholder-neutral-400 rounded-2xl focus:outline-none focus:border-teal-400 focus:ring-2 focus:ring-teal-500/20 transition-all"
                />
              </div>

              <div>
                <label for="phone" class="block text-base font-semibold text-neutral-700 mb-2">Телефон</label>
                <input
                  id="phone"
                  v-model="form.phone"
                  type="tel"
                  placeholder="+7 (___) ___-__-__"
                  class="w-full px-5 py-4 text-base bg-neutral-50 border-2 border-neutral-200 text-neutral-900 placeholder-neutral-400 rounded-2xl focus:outline-none focus:border-teal-400 focus:ring-2 focus:ring-teal-500/20 transition-all"
                />
              </div>

              <div>
                <label for="objectType" class="block text-base font-semibold text-neutral-700 mb-2">Тип объекта</label>
                <select
                  id="objectType"
                  v-model="form.objectType"
                  class="w-full px-5 py-4 text-base bg-neutral-50 border-2 border-neutral-200 text-neutral-900 rounded-2xl appearance-none cursor-pointer focus:outline-none focus:border-teal-400 focus:ring-2 focus:ring-teal-500/20 transition-all"
                >
                  <option value="" disabled class="text-neutral-400">Выберите тип объекта</option>
                  <option value="industrial">Промышленное здание</option>
                  <option value="administrative">Административное здание</option>
                  <option value="warehouse">Складской комплекс</option>
                  <option value="infrastructure">Инженерная инфраструктура</option>
                  <option value="turnkey">Возведение под ключ</option>
                  <option value="special_works">Отдельные виды работ</option>
                  <option value="other">Другое</option>
                </select>
              </div>

              <div v-if="form.objectType === 'turnkey'">
                <label for="turnkeyDetails" class="block text-base font-semibold text-neutral-700 mb-2">Какой объект необходимо возвести?</label>
                <input
                  id="turnkeyDetails"
                  v-model="form.otherDetails"
                  type="text"
                  placeholder="Например: Производственный цех 1500 м²"
                  class="w-full px-5 py-4 text-base bg-neutral-50 border-2 border-neutral-200 text-neutral-900 placeholder-neutral-400 rounded-2xl focus:outline-none focus:border-teal-400 focus:ring-2 focus:ring-teal-500/20 transition-all"
                />
              </div>

              <div v-if="form.objectType === 'special_works' || form.objectType === 'other'">
                <label for="otherDetails" class="block text-base font-semibold text-neutral-700 mb-2">Опишите, что именно нужно</label>
                <input
                  id="otherDetails"
                  v-model="form.otherDetails"
                  type="text"
                  placeholder="Напишите, какие именно работы вас интересуют"
                  class="w-full px-5 py-4 text-base bg-neutral-50 border-2 border-neutral-200 text-neutral-900 placeholder-neutral-400 rounded-2xl focus:outline-none focus:border-teal-400 focus:ring-2 focus:ring-teal-500/20 transition-all"
                />
              </div>

              <p v-if="error" class="text-red-500 text-base font-medium">{{ error }}</p>

              <button
                type="submit"
                :disabled="sending"
                class="w-full py-5 text-lg font-bold rounded-2xl bg-gradient-to-r from-teal-600 to-cyan-600 text-white shadow-xl shadow-teal-600/25 hover:shadow-teal-600/40 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer transition-all duration-300"
              >
                {{ sending ? 'Отправка...' : 'Отправить заявку' }}
              </button>
            </form>
          </div>
        </div>
      </div>
    </section>


    <!-- ══════════ FOOTER ══════════ -->
    <footer class="relative z-[1] bg-neutral-900 text-neutral-300">
      <div class="max-w-[1400px] mx-auto px-6 lg:px-10 py-16 lg:py-20">
        <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-10 lg:gap-12">

          <!-- col 1: company -->
          <div class="sm:col-span-2 lg:col-span-1">
            <div class="mb-5">
              <span class="block text-lg font-bold text-white">ПРАЙМ-СТРОЙ</span>
              <span class="block text-xs tracking-[0.15em] uppercase text-neutral-500">строительная компания</span>
            </div>
            <p class="text-base leading-relaxed text-neutral-400">
              Генеральный подрядчик полного цикла. Промышленное и&nbsp;гражданское строительство в&nbsp;Свердловской области.
            </p>
          </div>

          <!-- col 2: contacts -->
          <div>
            <h4 class="text-base font-bold text-white mb-5 uppercase tracking-wider">Контакты</h4>
            <ul class="space-y-4 text-base text-neutral-400">
              <li>
                <a href="tel:+79222011801" class="hover:text-teal-400 transition-colors">+7 (922) 201-18-01</a>
              </li>
              <li>
                <a href="mailto:office.prime-stroy@ya.ru" class="hover:text-teal-400 transition-colors">office.prime-stroy@ya.ru</a>
              </li>
              <li>г.&nbsp;Екатеринбург, ул.&nbsp;Барвинка,&nbsp;21, оф.&nbsp;35</li>
            </ul>
          </div>

          <!-- col 3: services -->
          <div>
            <h4 class="text-base font-bold text-white mb-5 uppercase tracking-wider">Услуги</h4>
            <ul class="space-y-3 text-base text-neutral-400">
              <li>Промышленные здания</li>
              <li>Фундаменты</li>
              <li>Металлоконструкции</li>
              <li>Промышленные полы</li>
              <li>Инженерные сети</li>
            </ul>
          </div>

          <!-- col 4: legal -->
          <div>
            <h4 class="text-base font-bold text-white mb-5 uppercase tracking-wider">Реквизиты</h4>
            <ul class="space-y-3 text-base text-neutral-400">
              <li>ООО СК «ПРАЙМ-СТРОЙ»</li>
              <li>ИНН 6671347890</li>
              <li class="break-all leading-relaxed">
                ЭДО Контур.Диадок:<br/>
                <span class="text-sm text-neutral-500">2BM-6671347890-667101001-202512220800083840444</span>
              </li>
            </ul>
          </div>
        </div>

        <div class="mt-14 pt-8 border-t border-neutral-800 flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-neutral-500">
          <span>&copy; {{ currentYear }} ООО СК «ПРАЙМ-СТРОЙ». Все права защищены.</span>
          <span>Екатеринбург, Свердловская область</span>
        </div>
      </div>
    </footer>
  </div>

  <!-- ══════════ SERVICE MODAL ══════════ -->
  <transition
    enter-active-class="transition-opacity duration-300"
    enter-from-class="opacity-0"
    enter-to-class="opacity-100"
    leave-active-class="transition-opacity duration-300"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
    <div v-if="selectedService" class="fixed inset-0 z-[100] flex items-center justify-center p-4 lg:p-10 bg-neutral-900/70 backdrop-blur-md" @click.self="selectedService = null">
      <div class="relative w-full max-w-6xl h-full max-h-[90vh] bg-white rounded-3xl overflow-hidden shadow-2xl flex flex-col md:flex-row">
        
        <!-- Close button -->
        <button @click="selectedService = null" class="absolute top-4 right-4 z-50 w-10 h-10 bg-white/90 shadow-sm backdrop-blur-md rounded-full flex items-center justify-center text-neutral-600 hover:text-teal-600 hover:bg-white hover:scale-110 transition-all">
          <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>
        </button>

        <!-- Left side: Images -->
        <div class="w-full md:w-1/2 bg-neutral-100 relative h-[40vh] md:h-auto border-r border-neutral-200/60">
          <div v-if="selectedService.images && selectedService.images.length" class="absolute inset-0 w-full h-full overflow-y-auto p-4 lg:p-8 flex flex-col gap-6">
            <img v-for="img in selectedService.images" :key="img" :src="'/' + img" class="w-full rounded-2xl object-cover shadow-md" alt="Фото работ" />
          </div>
        </div>

        <!-- Right side: Text and CTA -->
        <div class="w-full md:w-1/2 flex flex-col overflow-y-auto p-8 lg:p-12 bg-white">
          <h2 class="text-3xl lg:text-4xl font-black text-neutral-900 mb-6 leading-tight">{{ selectedService.title }}</h2>
          <p class="text-lg leading-relaxed text-neutral-600 mb-10 flex-grow">{{ selectedService.detailedDesc || selectedService.desc }}</p>
          
          <!-- CTA -->
          <div class="bg-gradient-to-br from-teal-50 to-cyan-50 border border-teal-100 rounded-3xl p-8 text-center mt-auto">
            <h3 class="text-xl lg:text-2xl font-bold text-neutral-900 mb-3">Готовы обсудить проект?</h3>
            <p class="text-neutral-600 mb-8 text-sm lg:text-base">Оставьте заявку, и наши инженеры свяжутся с вами для расчёта стоимости и сроков.</p>
            <button
              @click="closeModalAndScrollToContact"
              class="w-full py-4 lg:py-5 text-lg font-bold rounded-xl bg-gradient-to-r from-teal-600 to-cyan-600 text-white shadow-xl shadow-teal-600/25 hover:shadow-teal-600/40 hover:-translate-y-1 transition-all duration-300"
            >
              Оставить заявку
            </button>
          </div>
        </div>

      </div>
    </div>
  </transition>
</template>
