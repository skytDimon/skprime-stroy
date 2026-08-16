<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const currentYear = new Date().getFullYear()

/* ───── mobile nav ───── */
const mobileMenuOpen = ref(false)
const toggleMenu = () => { mobileMenuOpen.value = !mobileMenuOpen.value }

/* ───── header scroll shadow ───── */
const scrolled = ref(false)
function onScroll() { scrolled.value = window.scrollY > 20 }

/* ───── smooth scroll ───── */
function scrollTo(id) {
  mobileMenuOpen.value = false
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' })
}
function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

/* ───── stats animation ───── */
const statsYears = ref(0)
const statsObjects = ref(0)
const statsViolations = ref(0)
const statsSectionRef = ref(null)

let hasAnimated = false

function animateValue(obj, start, end, duration) {
  let startTimestamp = null;
  const step = (timestamp) => {
    if (!startTimestamp) startTimestamp = timestamp;
    let progress = Math.min((timestamp - startTimestamp) / duration, 1);
    
    obj.value = Math.floor(progress * (end - start) + start);
    if (progress < 1) {
      window.requestAnimationFrame(step);
    }
  };
  window.requestAnimationFrame(step);
}

onMounted(() => {
  window.addEventListener('scroll', onScroll)
  
  const observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting && !hasAnimated) {
      hasAnimated = true;
      animateValue(statsYears, 0, 8, 1500);
      animateValue(statsObjects, 0, 50, 1500);
      // violations stays 0, no need to animate
    }
  }, { threshold: 0.2 });
  
  if (statsSectionRef.value) {
    observer.observe(statsSectionRef.value);
  }
})

onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
})

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
    detailedDesc: `
      <p class="mb-6 text-2xl text-neutral-900 font-bold leading-snug">Мы выполняем полный цикл строительства складских, промышленных и административных объектов.</p>
      <p class="mb-6">Наши компетенции охватывают следующие виды работ и услуг:</p>
      <ul class="list-none space-y-3 mb-8 text-neutral-600">
        <li class="flex items-start gap-3"><span class="text-teal-500 mt-1">▪</span> <span>Проектирование</span></li>
        <li class="flex items-start gap-3"><span class="text-teal-500 mt-1">▪</span> <span>Входной контроль проектной документации</span></li>
        <li class="flex items-start gap-3"><span class="text-teal-500 mt-1">▪</span> <span>Подготовка к СМР и организация строительной площадки</span></li>
        <li class="flex items-start gap-3"><span class="text-teal-500 mt-1">▪</span> <span>Земляные работы</span></li>
        <li class="flex items-start gap-3"><span class="text-teal-500 mt-1">▪</span> <span>Устройство фундаментов любого типа и сложности</span></li>
        <li class="flex items-start gap-3"><span class="text-teal-500 mt-1">▪</span> <span>Возведение каркасов зданий</span></li>
        <li class="flex items-start gap-3"><span class="text-teal-500 mt-1">▪</span> <span>Монтаж ограждающих конструкций (в т.ч. светопрозрачных) и кровли, заполнение проемов</span></li>
        <li class="flex items-start gap-3"><span class="text-teal-500 mt-1">▪</span> <span>Промышленные полы</span></li>
        <li class="flex items-start gap-3"><span class="text-teal-500 mt-1">▪</span> <span>Внутренние и наружные инженерные сети</span></li>
        <li class="flex items-start gap-3"><span class="text-teal-500 mt-1">▪</span> <span>Чистовая отделка</span></li>
        <li class="flex items-start gap-3"><span class="text-teal-500 mt-1">▪</span> <span>Благоустройство территории</span></li>
      </ul>
    `,
    coverImage: '1.jpg',
    images: []
  },
  {
    title: 'Проектирование',
    desc: 'Разработка необходимых разделов проектной документации.',
    detailedDesc: `
      <p class="mb-6 text-xl">Мы понимаем, что качественный проект – это основа успешного и эффективного строительства, поэтому мы наладили прочное партнерство с ведущими проектными организациями, обладающими глубокой экспертизой в данной сфере.</p>
      
      <p class="mb-6 text-2xl font-bold text-neutral-900 mt-10">Почему мы работаем с партнерами по проектированию:</p>
      
      <ul class="space-y-6 mb-8 text-neutral-600">
        <li>
          <b class="text-neutral-900 block mb-2 text-lg">Специализированные знания</b>
          Наши партнеры – это узкопрофильные проектные бюро, команды архитекторов, конструкторов и инженеров, специализирующихся именно на промышленных, складских и административных объектах. Они досконально знают специфику таких зданий, нормативные требования (ГОСТы, СНиПы, СП) и последние тенденции в архитектуре и инженерии.
        </li>
        <li>
          <b class="text-neutral-900 block mb-2 text-lg">Инновационные решения</b>
          Партнеры регулярно внедряют новые технологии проектирования, используют современное программное обеспечение (BIM моделирование, 3D-визуализация), что позволяет создавать оптимальные, экономически эффективные и функциональные проекты.
        </li>
        <li>
          <b class="text-neutral-900 block mb-2 text-lg">Широкий спектр услуг</b>
          Мы можем предложить полный спектр проектных работ:
          <ul class="list-none space-y-3 mt-4">
            <li class="flex items-start gap-3"><span class="text-teal-500 mt-1">▪</span> <span><b>Архитектурное проектирование:</b> Разработка концепции, эскизных проектов, рабочих чертежей фасадов, планировок, интерьеров.</span></li>
            <li class="flex items-start gap-3"><span class="text-teal-500 mt-1">▪</span> <span><b>Конструктивные решения:</b> Проектирование несущих и ограждающих конструкций, фундаментов, каркасов зданий, расчет нагрузок.</span></li>
            <li class="flex items-start gap-3"><span class="text-teal-500 mt-1">▪</span> <span><b>Инженерные системы:</b> Проектирование систем отопления, вентиляции, водоснабжения, электроснабжения и слаботочных систем.</span></li>
            <li class="flex items-start gap-3"><span class="text-teal-500 mt-1">▪</span> <span><b>Проектирование технологических процессов:</b> Разработка схем размещения оборудования, планировок производственных зон.</span></li>
            <li class="flex items-start gap-3"><span class="text-teal-500 mt-1">▪</span> <span><b>Разработка документации:</b> Подготовка полного пакета документов для согласования и строительства.</span></li>
            <li class="flex items-start gap-3"><span class="text-teal-500 mt-1">▪</span> <span><b>Авторский надзор:</b> Сопровождение строительства для обеспечения соответствия работ проекту.</span></li>
          </ul>
        </li>
        <li>
          <b class="text-neutral-900 block mb-2 text-lg">Оптимизация сроков и бюджета</b>
          Благодаря слаженной работе нашей строительной компании и проектных партнеров, процесс от идеи до реализации становится более быстрым и предсказуемым.
        </li>
        <li>
          <b class="text-neutral-900 block mb-2 text-lg">Индивидуальный подход</b>
          Мы вместе с нашими партнерами внимательно изучаем потребности каждого клиента, специфику его бизнеса и требования к будущему объекту.
        </li>
      </ul>
      
      <p class="mb-6 text-2xl font-bold text-neutral-900 mt-12">Процесс проектирования:</p>
      
      <ol class="list-decimal pl-6 space-y-4 mb-8 text-neutral-600 marker:text-teal-600 marker:font-bold">
        <li><b class="text-neutral-900">Обсуждение требований:</b> Вы формулируете свои задачи, цели и пожелания к будущему зданию.</li>
        <li><b class="text-neutral-900">Предпроектная проработка:</b> Наши специалисты анализируют ваши потребности, проводят обследование участка, изучают технические условия.</li>
        <li><b class="text-neutral-900">Разработка концепции и эскизного проекта:</b> Формируется видение будущего здания, основные планировочные и архитектурные решения.</li>
        <li><b class="text-neutral-900">Создание проектной документации:</b> Детальная разработка всех разделов проекта.</li>
        <li><b class="text-neutral-900">Согласование проекта:</b> Прохождение экспертизы и получение необходимых разрешений.</li>
        <li><b class="text-neutral-900">Передача рабочей документации:</b> Подготовка полного комплекта чертежей и спецификаций для строителей.</li>
      </ol>
      
      <p class="mt-8 p-6 bg-neutral-50 rounded-2xl border border-neutral-100 italic">Мы гарантируем, что привлечение наших проверенных партнеров по проектированию позволит вам получить не просто здание, а идеально спроектированное пространство, максимально отвечающее вашим производственным, логистическим или административным задачам.</p>
    `,
    coverImage: 'background.jpg',
    images: []
  },
  {
    title: 'Организация строительной площадки',
    desc: 'Полный комплекс мероприятий, нацеленных на безопасное, быстрое и эффективное выполнение всех видов работ на объекте.',
    detailedDesc: `
      <p class="mb-6 text-xl">Начало любого строительства – это не только завоз техники и материалов, но и тщательная подготовительная работа на месте будущей стройки. Правильная организация и подготовка строительной площадки являются фундаментом для дальнейшего эффективного, безопасного и своевременного выполнения всех строительно-монтажных работ.</p>
      
      <p class="mb-6 text-2xl font-bold text-neutral-900 mt-10">Основные этапы подготовки:</p>
      
      <ul class="space-y-8 mb-8 text-neutral-600">
        <li>
          <b class="text-neutral-900 block mb-2 text-lg">1. Освобождение территории</b>
          <ul class="list-none space-y-2 mt-3 pl-2 border-l-2 border-teal-100">
            <li class="pl-4">▪ Демонтаж существующих зданий и сооружений: аккуратный демонтаж и утилизация мусора.</li>
            <li class="pl-4">▪ Снос зеленых насаждений: удаление деревьев и кустарников с соблюдением экологических норм.</li>
            <li class="pl-4">▪ Перенос коммуникаций: временное или постоянное отключение и перенос существующих сетей.</li>
          </ul>
        </li>
        <li>
          <b class="text-neutral-900 block mb-2 text-lg">2. Ограждение строительной площадки</b>
          <ul class="list-none space-y-2 mt-3 pl-2 border-l-2 border-teal-100">
            <li class="pl-4">▪ Назначение: обеспечение безопасности, предотвращение несанкционированного доступа.</li>
            <li class="pl-4">▪ Типы ограждений: временные (из сетки, профлиста) или капитальные.</li>
            <li class="pl-4">▪ Организация входов/выездов: оборудование КПП, организация въездов с мойкой колес.</li>
          </ul>
        </li>
        <li>
          <b class="text-neutral-900 block mb-2 text-lg">3. Планировка территории</b>
          <ul class="list-none space-y-2 mt-3 pl-2 border-l-2 border-teal-100">
            <li class="pl-4">▪ Вертикальная планировка: придание рельефу нужной формы, выравнивание пятна застройки.</li>
            <li class="pl-4">▪ Разбивка осей здания: вынос в натуру основных геодезических осей будущего здания.</li>
          </ul>
        </li>
        <li>
          <b class="text-neutral-900 block mb-2 text-lg">4. Временные сооружения и инфраструктура</b>
          <ul class="list-none space-y-2 mt-3 pl-2 border-l-2 border-teal-100">
            <li class="pl-4">▪ Строительный городок: размещение бытовых помещений, складов.</li>
            <li class="pl-4">▪ Временные инженерные сети: электроснабжение, водоснабжение, канализация, освещение.</li>
            <li class="pl-4">▪ Устройство подъездных путей: создание временных дорог.</li>
          </ul>
        </li>
        <li>
          <b class="text-neutral-900 block mb-2 text-lg">5. Обеспечение безопасности и экологичности</b>
          <ul class="list-none space-y-2 mt-3 pl-2 border-l-2 border-teal-100">
            <li class="pl-4">▪ Информационные щиты: установка стендов с информацией об объекте.</li>
            <li class="pl-4">▪ Противопожарные мероприятия: размещение первичных средств пожаротушения.</li>
            <li class="pl-4">▪ Экологический контроль: контроль за пылеобразованием и шумом, сбор отходов.</li>
          </ul>
        </li>
      </ul>
      
      <p class="mb-6 text-2xl font-bold text-neutral-900 mt-12">Важность грамотной подготовки:</p>
      
      <ul class="list-none space-y-3 mb-8 text-neutral-600">
        <li class="flex items-start gap-3"><span class="text-teal-500 mt-1 font-bold">✓</span> <span><b>Соблюдение сроков:</b> Четкая организация позволяет избежать простоев.</span></li>
        <li class="flex items-start gap-3"><span class="text-teal-500 mt-1 font-bold">✓</span> <span><b>Снижение затрат:</b> Эффективное использование ресурсов, минимизация потерь.</span></li>
        <li class="flex items-start gap-3"><span class="text-teal-500 mt-1 font-bold">✓</span> <span><b>Обеспечение безопасности:</b> Предотвращение несчастных случаев на стройплощадке.</span></li>
        <li class="flex items-start gap-3"><span class="text-teal-500 mt-1 font-bold">✓</span> <span><b>Качество строительства:</b> Правильная разбивка и планировка – основа для точного возведения.</span></li>
      </ul>
    `,
    coverImage: '3.jpg',
    images: []
  },
  {
    title: 'Фундаменты',
    desc: 'Устройство ленточных, столбчатых, плитных и свайно-ростверковых фундаментов, а также фундаментов под оборудование.',
    detailedDesc: `
      <p class="mb-6 text-2xl text-neutral-900 font-bold leading-snug">Качественный фундамент — основа надежности и долговечности зданий и сооружений.</p>
      <p class="mb-6 text-lg">Промышленные здания и сооружения – это сложные инженерные конструкции, от надежности которых напрямую зависит безопасность производства, сохранность оборудования и долговечность всего объекта. Центральное место в этой системе занимает фундамент – основа, принимающая на себя все нагрузки и передающая их грунту.</p>
      
      <p class="mb-6 text-xl font-bold text-neutral-900 mt-10">Специфика промышленных фундаментов:</p>
      
      <div class="grid sm:grid-cols-2 gap-6 mb-10">
        <div class="bg-neutral-50 p-6 rounded-2xl border border-neutral-100">
          <b class="text-neutral-900 block mb-2">Высокие нагрузки</b>
          <span class="text-neutral-600 text-sm">Промышленные объекты эксплуатируются под значительными нагрузками от тяжелого оборудования.</span>
        </div>
        <div class="bg-neutral-50 p-6 rounded-2xl border border-neutral-100">
          <b class="text-neutral-900 block mb-2">Динамические воздействия</b>
          <span class="text-neutral-600 text-sm">Работа машин и механизмов создает вибрации, которые необходимо учитывать.</span>
        </div>
        <div class="bg-neutral-50 p-6 rounded-2xl border border-neutral-100">
          <b class="text-neutral-900 block mb-2">Условия эксплуатации</b>
          <span class="text-neutral-600 text-sm">Особые геологические условия требуют применения специальных технологий и материалов.</span>
        </div>
        <div class="bg-neutral-50 p-6 rounded-2xl border border-neutral-100">
          <b class="text-neutral-900 block mb-2">Требования к точности</b>
          <span class="text-neutral-600 text-sm">Установка оборудования требует высокой геометрической точности фундамента.</span>
        </div>
      </div>
      
      <p class="mb-6 text-xl font-bold text-neutral-900">Виды фундаментов:</p>
      <ul class="space-y-4 mb-8 text-neutral-600">
        <li><b class="text-neutral-900">Ленточные:</b> Бетонные ленты под несущими стенами и колоннами.</li>
        <li><b class="text-neutral-900">Столбчатые:</b> Отдельные столбы с ростверком. Для облегченных конструкций.</li>
        <li><b class="text-neutral-900">Плитные:</b> Сплошная ж/б плита под всем зданием. Идеальны для слабых грунтов.</li>
        <li><b class="text-neutral-900">Свайные:</b> Забивные или винтовые сваи до несущего слоя грунта.</li>
        <li><b class="text-neutral-900">Под оборудование:</b> Специальные конструкции для вибрационных нагрузок.</li>
      </ul>
      
      <p class="mb-6 text-xl font-bold text-neutral-900 mt-10">Этапы строительства:</p>
      <div class="flex flex-wrap gap-3 mb-8">
        <span class="px-4 py-2 bg-teal-50 text-teal-700 rounded-full text-sm font-semibold">Изыскания</span>
        <span class="px-4 py-2 bg-teal-50 text-teal-700 rounded-full text-sm font-semibold">Проектирование</span>
        <span class="px-4 py-2 bg-teal-50 text-teal-700 rounded-full text-sm font-semibold">Земляные работы</span>
        <span class="px-4 py-2 bg-teal-50 text-teal-700 rounded-full text-sm font-semibold">Опалубка</span>
        <span class="px-4 py-2 bg-teal-50 text-teal-700 rounded-full text-sm font-semibold">Армирование</span>
        <span class="px-4 py-2 bg-teal-50 text-teal-700 rounded-full text-sm font-semibold">Бетонирование</span>
        <span class="px-4 py-2 bg-teal-50 text-teal-700 rounded-full text-sm font-semibold">Гидроизоляция</span>
      </div>
    `,
    coverImage: '2.png',
    images: ['2.png']
  },
  {
    title: 'Металлические и железобетонные каркасы',
    desc: 'Изготовление и монтаж металлических конструкций по КМД, возведение сборных и монолитных железобетонных каркасов.',
    detailedDesc: `
      <p class="mb-6 text-xl text-neutral-900 font-bold">Производим сборку и надежный монтаж металлических и железобетонных конструкций.</p>
      <p class="mb-8">Каркас здания – это его скелет, несущая система, которая воспринимает все нагрузки и передает их на фундамент. От правильного выбора материала и типа каркаса зависит прочность, долговечность, скорость строительства и стоимость здания.</p>
      
      <div class="space-y-10">
        <div>
          <h4 class="text-2xl font-black text-neutral-900 mb-4 flex items-center gap-3">
            <span class="w-2 h-8 bg-teal-500 rounded-full"></span> Металлические каркасы
          </h4>
          <p class="mb-4 text-neutral-600">Высокотехнологичное решение, отличающееся прочностью, долговечностью и скоростью монтажа. Идеально для промышленных зданий, ангаров, торговых центров.</p>
          <div class="bg-neutral-50 p-6 rounded-2xl border border-neutral-100">
            <b class="text-teal-700 block mb-2">Преимущества:</b>
            <p class="text-sm text-neutral-600">Высокая прочность, скорость монтажа, адаптивность, большие пролеты, сейсмоустойчивость.</p>
          </div>
        </div>
        
        <div>
          <h4 class="text-2xl font-black text-neutral-900 mb-4 flex items-center gap-3">
            <span class="w-2 h-8 bg-cyan-500 rounded-full"></span> Монолитный железобетон
          </h4>
          <p class="mb-4 text-neutral-600">Бетон, армированный стальными стержнями, который заливается непосредственно на стройплощадке. Подходит для многоэтажных и административных зданий.</p>
          <div class="bg-neutral-50 p-6 rounded-2xl border border-neutral-100">
            <b class="text-cyan-700 block mb-2">Преимущества:</b>
            <p class="text-sm text-neutral-600">Монолитность конструкции, высокая несущая способность, свобода архитектурных форм, долговечность, огнестойкость.</p>
          </div>
        </div>
        
        <div>
          <h4 class="text-2xl font-black text-neutral-900 mb-4 flex items-center gap-3">
            <span class="w-2 h-8 bg-blue-500 rounded-full"></span> Сборный железобетон
          </h4>
          <p class="mb-4 text-neutral-600">Конструкции, изготовленные из железобетона на заводе, монтируемые на стройплощадке. Оптимально для массового строительства, типовых складов.</p>
          <div class="bg-neutral-50 p-6 rounded-2xl border border-neutral-100">
            <b class="text-blue-700 block mb-2">Преимущества:</b>
            <p class="text-sm text-neutral-600">Высокая скорость монтажа, строгий заводской контроль качества, независимость от погодных условий.</p>
          </div>
        </div>
      </div>
    `,
    coverImage: '3.jpg',
    images: ['3.jpg']
  },
  {
    title: 'Ограждающие конструкции',
    desc: 'Энергоэффективная и привлекательная «рубашка» для вашего здания.',
    detailedDesc: `
      <p class="mb-6 text-lg">Ограждающие конструкции – это внешние и внутренние стены, перекрытия и кровля, которые формируют оболочку здания, разделяют его на функциональные зоны и обеспечивают защиту от внешних воздействий.</p>
      
      <p class="font-bold text-2xl text-neutral-900 mt-10 mb-8">Основные решения для промышленных зданий:</p>
      
      <div class="space-y-6">
        <div class="border-b border-neutral-100 pb-6">
          <p class="font-black text-xl text-neutral-900 mb-2">Сэндвич-панели</p>
          <p class="mb-4 text-neutral-600 text-sm">Трехслойные панели, состоящие из двух слоев облицовки и утеплителя (минвата, ПИР, ПУР).</p>
          <p class="text-neutral-600 text-sm"><b class="text-neutral-800">Плюсы:</b> Быстрый монтаж, высокая теплоизоляция, долговечность, эстетика.</p>
        </div>

        <div class="border-b border-neutral-100 pb-6">
          <p class="font-black text-xl text-neutral-900 mb-2">Профилированный лист (металлопрофиль)</p>
          <p class="mb-4 text-neutral-600 text-sm">Стальные листы с гофрированным профилем. Часто используются с утеплением.</p>
          <p class="text-neutral-600 text-sm"><b class="text-neutral-800">Плюсы:</b> Низкая стоимость, высокая скорость монтажа, долговечность.</p>
        </div>

        <div class="border-b border-neutral-100 pb-6">
          <p class="font-black text-xl text-neutral-900 mb-2">Железобетонные панели</p>
          <p class="mb-4 text-neutral-600 text-sm">Сборные ж/б плиты заводского изготовления, могут быть с утеплителем.</p>
          <p class="text-neutral-600 text-sm"><b class="text-neutral-800">Плюсы:</b> Сверхпрочность, антивандальность, негорючесть.</p>
        </div>

        <div>
          <p class="font-black text-xl text-neutral-900 mb-2">Комбинированные фасады</p>
          <p class="mb-4 text-neutral-600 text-sm">Традиционные материалы (кирпич, керамогранит) в сочетании с витражным остеклением и сэндвич-панелями. Применяются для придания административным корпусам современного и статусного вида.</p>
        </div>
      </div>
    `,
    coverImage: '6.jpg',
    images: []
  },
  {
    title: 'Промышленные полы',
    desc: 'Устройство бетонных топпинговых, эпоксидных, полиуретановых промышленных полов',
    detailedDesc: `
      <p class="mb-6 text-xl text-neutral-900 font-bold">Создаем высокопрочные промышленные полы, способные выдерживать колоссальные нагрузки.</p>
      
      <p class="mb-8">Промышленные полы – это важнейший элемент производственной инфраструктуры. Они выдерживают интенсивную эксплуатацию, воздействие агрессивных сред и обеспечивают безопасность персонала.</p>
      
      <h4 class="font-black text-2xl text-neutral-900 mt-10 mb-6">Типы промышленных полов:</h4>
      
      <div class="grid sm:grid-cols-3 gap-6 mb-10">
        <div class="bg-white border-2 border-neutral-100 rounded-2xl p-6 shadow-sm hover:shadow-md transition-shadow">
          <div class="w-12 h-12 bg-neutral-100 rounded-xl flex items-center justify-center text-2xl mb-4 text-neutral-400">1</div>
          <b class="text-neutral-900 block mb-3 text-lg">Бетонные полы с топпингом</b>
          <p class="text-neutral-600 text-sm leading-relaxed mb-4">Бетонная стяжка, верхний слой которой упрочняется специальными смесями.</p>
          <p class="text-xs text-neutral-500 bg-neutral-50 p-3 rounded-lg"><b>Применение:</b> склады, цеха, гаражи.</p>
        </div>
        
        <div class="bg-white border-2 border-neutral-100 rounded-2xl p-6 shadow-sm hover:shadow-md transition-shadow">
          <div class="w-12 h-12 bg-teal-50 rounded-xl flex items-center justify-center text-2xl mb-4 text-teal-500">2</div>
          <b class="text-neutral-900 block mb-3 text-lg">Эпоксидные наливные полы</b>
          <p class="text-neutral-600 text-sm leading-relaxed mb-4">Образуют гладкое, бесшовное, химически стойкое и гигиеничное покрытие.</p>
          <p class="text-xs text-neutral-500 bg-neutral-50 p-3 rounded-lg"><b>Применение:</b> пищевая, хим. промышленность.</p>
        </div>
        
        <div class="bg-white border-2 border-neutral-100 rounded-2xl p-6 shadow-sm hover:shadow-md transition-shadow">
          <div class="w-12 h-12 bg-cyan-50 rounded-xl flex items-center justify-center text-2xl mb-4 text-cyan-500">3</div>
          <b class="text-neutral-900 block mb-3 text-lg">Полиуретановые полы</b>
          <p class="text-neutral-600 text-sm leading-relaxed mb-4">Отличаются высокой эластичностью и устойчивостью к температурным перепадам.</p>
          <p class="text-xs text-neutral-500 bg-neutral-50 p-3 rounded-lg"><b>Применение:</b> холодильные камеры.</p>
        </div>
      </div>
      
      <p class="font-bold text-neutral-900 mt-6 mb-2">Этапы устройства полов:</p>
      <p class="text-neutral-600">Подготовка основания, устройство гидроизоляции, укладка утеплителя и арматуры, заливка бетона с финишной обработкой (втирание топпинга или заливка полимерного состава), нарезка швов.</p>
    `,
    coverImage: '4.jpg',
    images: ['44.jpg']
  },
  {
    title: 'Инженерные сети',
    desc: 'Проектирование и монтаж наружных и внутренних инженерных сетей: водоснабжение, канализация, отопление, вентиляция, электроснабжение.',
    detailedDesc: `
      <p class="mb-8 text-xl">Выполняем полный комплекс работ по устройству внутренних и наружных инженерных коммуникаций, обеспечивающих функционирование любого промышленного или административного здания.</p>
      
      <h4 class="font-black text-2xl text-neutral-900 mb-8">Монтаж наружных и внутренних систем:</h4>
      
      <ul class="space-y-6 text-neutral-600">
        <li class="flex gap-4">
          <div class="w-10 h-10 shrink-0 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center font-bold">1</div>
          <div>
            <b class="text-neutral-900 text-lg block mb-1">Водоснабжение и Канализация</b>
            <p class="text-sm">Подача воды для технологических нужд и санитарных целей. Отвод промышленных и бытовых стоков, установка локальных очистных сооружений (ЛОС).</p>
          </div>
        </li>
        <li class="flex gap-4">
          <div class="w-10 h-10 shrink-0 bg-rose-50 text-rose-600 rounded-full flex items-center justify-center font-bold">2</div>
          <div>
            <b class="text-neutral-900 text-lg block mb-1">Отопление</b>
            <p class="text-sm">Обустройство теплотрасс, ИТП, монтаж радиаторов, фанкойлов и мощных воздушных отопителей для цехов.</p>
          </div>
        </li>
        <li class="flex gap-4">
          <div class="w-10 h-10 shrink-0 bg-teal-50 text-teal-600 rounded-full flex items-center justify-center font-bold">3</div>
          <div>
            <b class="text-neutral-900 text-lg block mb-1">Вентиляция и кондиционирование</b>
            <p class="text-sm">Мощные вытяжные системы, аспирация для удаления пыли, системы рекуперации и поддержания микроклимата.</p>
          </div>
        </li>
        <li class="flex gap-4">
          <div class="w-10 h-10 shrink-0 bg-amber-50 text-amber-600 rounded-full flex items-center justify-center font-bold">4</div>
          <div>
            <b class="text-neutral-900 text-lg block mb-1">Электроснабжение и Слаботочные сети</b>
            <p class="text-sm">Установка ТП, ГРЩ, ВРУ, прокладка силовых линий для тяжелого оборудования. Интеграция систем АСУ ТП, СКУД, пожарной сигнализации и видеонаблюдения.</p>
          </div>
        </li>
      </ul>
      
      <p class="mt-10 p-6 bg-teal-50/50 rounded-2xl border border-teal-100 text-teal-900 text-sm">Проектирование и монтаж инженерных сетей требуют глубоких знаний и строгого соблюдения строительных норм и правил (СНиП, ГОСТ, СП). Комплексное проектирование является залогом надежной и эффективной работы здания.</p>
    `,
    coverImage: '5.png',
    images: ['55.png'],
    bgPosition: 'center 60%'
  }
]
</script>

<template>
  <div class="relative min-h-screen text-neutral-900 antialiased" style="font-family: 'Inter', system-ui, sans-serif;">
    <!-- background image -->
    <div class="fixed inset-0 z-0 pointer-events-none" style="background: url('/background.jpg') center / cover no-repeat fixed;"></div>

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
            <img src="/logo.png" alt="ПРАЙМ-СТРОЙ" loading="lazy" class="w-20 h-20 lg:w-24 lg:h-24 rounded-2xl object-contain" />
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
            <div class="hidden md:flex items-center gap-3">
              <div class="w-12 h-12 rounded-xl flex items-center justify-center bg-teal-50 text-teal-600 shrink-0">
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
              </div>
              <div class="flex flex-col">
                <a href="tel:+73433002500" class="text-base font-bold text-teal-700 hover:text-teal-500 transition-colors leading-tight">+7 (343) 300-25-00</a>
                <a href="tel:+79222011801" class="text-sm font-semibold text-teal-600/80 hover:text-teal-500 transition-colors leading-tight mt-0.5">+7 (922) 201-18-01</a>
              </div>
            </div>

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
            <div class="flex flex-col gap-1 py-3">
              <a href="tel:+73433002500" class="text-lg font-bold text-teal-700">+7 (343) 300-25-00</a>
              <a href="tel:+79222011801" class="text-base font-semibold text-teal-600">+7 (922) 201-18-01</a>
            </div>
          </div>
        </div>
      </transition>
    </header>


    <!-- ══════════ HERO ══════════ -->
    <section class="relative z-[1] min-h-screen flex items-center overflow-hidden">


      <div class="relative w-full max-w-[1400px] mx-auto px-6 lg:px-10 py-36 lg:py-44 z-10">
        <div class="max-w-4xl">
          <div class="inline-flex items-center gap-3 px-5 py-2 rounded-full text-sm font-semibold mb-10 bg-teal-50 border border-teal-200 text-teal-700">
            <span class="w-2.5 h-2.5 rounded-full bg-teal-500 animate-pulse"></span>
            Екатеринбург и Свердловская область
          </div>

          <h1 class="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-black leading-[1.1] tracking-tight text-neutral-900">
            Строим промышленные<br/>объекты
            <span class="text-teal-600"> точно в&nbsp;срок</span>
          </h1>

          <p class="mt-8 lg:mt-10 text-lg lg:text-xl leading-relaxed max-w-3xl text-neutral-800 font-medium">
            Строительная компания «ПРАЙМ-СТРОЙ» - генеральный подрядчик полного цикла. Наша миссия – создавать современные, функциональные и безопасные объекты, которые способствуют развитию бизнеса наших клиентов и улучшению качества жизни общества. Мы стремимся быть не просто подрядчиком, а надежным партнером, на которого можно положиться на каждом этапе реализации проекта.
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
          <div ref="statsSectionRef" class="mt-16 lg:mt-20 grid grid-cols-3 gap-8 lg:gap-12 max-w-xl">
            <div>
              <div class="text-5xl lg:text-6xl font-black text-neutral-900 tracking-tight">{{ statsYears }}+</div>
              <div class="text-sm lg:text-base mt-2 text-neutral-400">лет на рынке</div>
            </div>
            <div>
              <div class="text-5xl lg:text-6xl font-black text-neutral-900 tracking-tight">{{ statsObjects }}+</div>
              <div class="text-sm lg:text-base mt-2 text-neutral-400">объектов сдано</div>
            </div>
            <div class="col-span-2 md:col-span-1 text-center md:text-left mt-4 md:mt-0">
              <div class="text-5xl lg:text-6xl font-black text-neutral-900 tracking-tight">{{ statsViolations }}</div>
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
        <div class="max-w-5xl">
          <div v-fade-in style="text-shadow: 0 0 15px rgba(255,255,255,1), 0 0 30px rgba(255,255,255,1), 0 0 5px rgba(255,255,255,1);">
            <span class="text-sm lg:text-base font-bold tracking-[0.2em] uppercase text-teal-600">О компании</span>
            <h2 class="mt-4 text-3xl sm:text-4xl lg:text-5xl font-black tracking-tight leading-tight text-neutral-900">
              Надёжный <span class="text-teal-600" style="text-shadow: 0 0 15px rgba(255,255,255,1);">генеральный подрядчик</span><br class="hidden lg:block"/>
              для промышленного строительства под&nbsp;ключ
            </h2>
            <p class="mt-8 text-base sm:text-lg leading-relaxed text-neutral-800 font-semibold">
              Строительная компания «ПРАЙМ-СТРОЙ» - это динамично развивающаяся строительная компания, специализирующаяся на возведении логистических комплексов, промышленных и административных зданий и сооружений любой сложности. Мы объединяем многолетний опыт, передовые технологии и команду высококвалифицированных профессионалов, чтобы предложить нашим клиентам комплексные решения – от проектирования до сдачи объекта "под ключ".
            </p>
            
            <div class="mt-8 space-y-8">
              <div>
                <h3 class="text-xl font-bold text-neutral-900 mb-4">Что нас отличает:</h3>
                <ul class="space-y-3 text-neutral-800 font-medium">
                  <li class="flex items-start gap-3"><span class="text-teal-600 font-bold mt-0.5">✓</span> <span><b>Комплексный подход:</b> полный цикл строительных работ, включая подготовку, СМР, сети и благоустройство.</span></li>
                  <li class="flex items-start gap-3"><span class="text-teal-600 font-bold mt-0.5">✓</span> <span><b>Опыт и экспертиза:</b> команда из опытных инженеров, строителей и менеджеров проектов.</span></li>
                  <li class="flex items-start gap-3"><span class="text-teal-600 font-bold mt-0.5">✓</span> <span><b>Современные технологии:</b> инновационные материалы для оптимизации сроков и энергоэффективности.</span></li>
                  <li class="flex items-start gap-3"><span class="text-teal-600 font-bold mt-0.5">✓</span> <span><b>Строгий контроль:</b> многоуровневая проверка качества, допуски СРО, работа по ГОСТ, СНиП, СП.</span></li>
                  <li class="flex items-start gap-3"><span class="text-teal-600 font-bold mt-0.5">✓</span> <span><b>Ответственность и прозрачность:</b> честность, открытое обсуждение финансовых вопросов и этапов.</span></li>
                  <li class="flex items-start gap-3"><span class="text-teal-600 font-bold mt-0.5">✓</span> <span><b>Безопасность:</b> соблюдение правил охраны труда является безусловным приоритетом.</span></li>
                </ul>
              </div>

              <div>
                <h3 class="text-xl font-bold text-neutral-900 mb-4">Наши ключевые направления:</h3>
                <ul class="space-y-2 text-neutral-800 font-medium">
                  <li class="flex items-start gap-3"><span class="w-1.5 h-1.5 rounded-full bg-teal-500 mt-2.5 shrink-0"></span> <span>Возведение складских комплексов и логистических центров</span></li>
                  <li class="flex items-start gap-3"><span class="w-1.5 h-1.5 rounded-full bg-teal-500 mt-2.5 shrink-0"></span> <span>Строительство офисных зданий и бизнес-центров</span></li>
                  <li class="flex items-start gap-3"><span class="w-1.5 h-1.5 rounded-full bg-teal-500 mt-2.5 shrink-0"></span> <span>Создание торговых комплексов и выставочных павильонов</span></li>
                  <li class="flex items-start gap-3"><span class="w-1.5 h-1.5 rounded-full bg-teal-500 mt-2.5 shrink-0"></span> <span>Реконструкция и модернизация промышленных и административных объектов</span></li>
                  <li class="flex items-start gap-3"><span class="w-1.5 h-1.5 rounded-full bg-teal-500 mt-2.5 shrink-0"></span> <span>Монтаж металлоконструкций и ограждающих конструкций</span></li>
                  <li class="flex items-start gap-3"><span class="w-1.5 h-1.5 rounded-full bg-teal-500 mt-2.5 shrink-0"></span> <span>Устройство промышленных полов и монтаж инженерных сетей</span></li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>


    <!-- ══════════ SERVICES ══════════ -->
    <section id="services" class="relative z-[1] py-24 lg:py-32">
      <div class="max-w-[1400px] mx-auto px-6 lg:px-10">
        <div v-fade-in class="text-center mb-16 lg:mb-20" style="text-shadow: 0 0 15px rgba(255,255,255,1), 0 0 30px rgba(255,255,255,1), 0 0 5px rgba(255,255,255,1);">
          <span class="text-sm lg:text-base font-bold tracking-[0.2em] uppercase text-teal-600">Компетенции</span>
          <h2 class="mt-4 text-3xl sm:text-4xl lg:text-5xl font-black tracking-tight text-neutral-900">
            Комплексные решения<br class="hidden sm:block"/> для&nbsp;вашего объекта
          </h2>
          <p class="mt-6 max-w-3xl mx-auto text-lg text-neutral-800 font-semibold">
            Выполняем весь спектр строительно-монтажных работ собственными аттестованными бригадами. Каждый этап — под контролем ИТР и с оформлением исполнительной документации.
          </p>
        </div>

        <div class="grid md:grid-cols-2 xl:grid-cols-3 gap-6 lg:gap-8">
          <div
            v-for="(s, i) in services"
            :key="i"
            @click="selectedService = s"
            class="group relative bg-white border-2 border-neutral-200 rounded-3xl overflow-hidden shadow-lg hover:shadow-teal-900/10 hover:border-teal-400/60 hover:-translate-y-2 transition-all duration-300 cursor-pointer min-h-[350px] md:min-h-[420px] flex flex-col justify-end"
            :class="{ 'md:col-span-2 xl:col-span-3': i === 0 || i === 7 }"
            v-fade-in
          >
            <!-- background image -->
            <div class="absolute inset-0 z-0 bg-cover transition-transform duration-700 group-hover:scale-105" :style="{ backgroundImage: `url('/${s.coverImage}')`, backgroundPosition: s.bgPosition || 'top' }"></div>

            <!-- gradient for text readability -->
            <div class="absolute inset-0 z-0 bg-gradient-to-t from-white via-white/80 to-transparent"></div>

            <div class="relative z-10 p-8 lg:p-10 pt-20 mt-auto">
              <h3 class="text-xl lg:text-2xl font-black text-neutral-900 mb-4">{{ s.title }}</h3>
              <p class="text-base lg:text-lg leading-relaxed font-semibold text-neutral-900">{{ s.desc }}</p>
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
          <div v-fade-in>
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
                  <div class="flex flex-col mt-1">
                    <a href="mailto:info@skprime-stroy.ru" class="text-base text-teal-600 hover:text-teal-500 transition-colors">info@skprime-stroy.ru</a>
                    <a href="mailto:office.prime-stroy@ya.ru" class="text-sm text-teal-600/80 hover:text-teal-500 transition-colors">office.prime-stroy@ya.ru</a>
                  </div>
                </div>
              </div>

              <div class="flex items-start gap-5">
                <div class="w-14 h-14 rounded-2xl bg-neutral-100 text-teal-600 flex items-center justify-center shrink-0">
                  <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
                </div>
                <div>
                  <div class="font-bold text-lg text-neutral-900">Телефон</div>
                  <div class="flex flex-col mt-1 gap-1">
                    <a href="tel:+73433002500" class="text-base text-teal-700 font-semibold hover:text-teal-500 transition-colors">+7 (343) 300-25-00</a>
                    <a href="tel:+79222011801" class="text-sm text-teal-600 hover:text-teal-500 transition-colors">+7 (922) 201-18-01</a>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- right: form -->
          <div v-fade-in class="bg-white border-2 border-neutral-200 rounded-3xl p-8 lg:p-10 shadow-xl shadow-neutral-200/50">

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
              <li class="flex flex-col gap-1">
                <a href="tel:+73433002500" class="hover:text-teal-400 transition-colors text-white">+7 (343) 300-25-00</a>
                <a href="tel:+79222011801" class="hover:text-teal-400 transition-colors text-sm">+7 (922) 201-18-01</a>
              </li>
              <li class="flex flex-col gap-1">
                <a href="mailto:info@skprime-stroy.ru" class="hover:text-teal-400 transition-colors text-white">info@skprime-stroy.ru</a>
                <a href="mailto:office.prime-stroy@ya.ru" class="hover:text-teal-400 transition-colors text-sm">office.prime-stroy@ya.ru</a>
              </li>
              <li>г.&nbsp;Екатеринбург, ул.&nbsp;Барвинка,&nbsp;21, оф.&nbsp;35</li>
            </ul>
          </div>

          <!-- col 3: services -->
          <div>
            <h4 class="text-base font-bold text-white mb-5 uppercase tracking-wider">Услуги</h4>
            <ul class="space-y-2 text-sm text-neutral-400">
              <li>Проектирование</li>
              <li>Подготовка и земляные работы</li>
              <li>Устройство фундаментов</li>
              <li>Монтаж каркасов (металл, ж/б)</li>
              <li>Ограждающие конструкции</li>
              <li>Промышленные полы</li>
              <li>Инженерные сети</li>
              <li>Отделка и благоустройство</li>
            </ul>
          </div>

          <!-- col 4: legal -->
          <div>
            <h4 class="text-base font-bold text-white mb-5 uppercase tracking-wider">Реквизиты</h4>
            <ul class="space-y-3 text-base text-neutral-400 mb-6">
              <li>ООО СК «ПРАЙМ-СТРОЙ»</li>
              <li>ИНН 6671347890</li>
              <li class="break-all leading-relaxed">
                ЭДО Контур.Диадок:<br/>
                <span class="text-sm text-neutral-500">2BM-6671347890-667101001-202512220800083840444</span>
              </li>
            </ul>
            <div class="flex flex-col gap-3 items-start">
              <a href="/req1.docx" download class="inline-flex items-center gap-2 px-5 py-3 text-sm font-bold rounded-xl bg-teal-600/10 text-teal-400 hover:bg-teal-600/20 transition-all border border-teal-600/20">
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
                Скачать реквизиты
              </a>
              <a href="/req.pdf" target="_blank" download="Выписка_СРО_ПРАЙМ-СТРОЙ.pdf" class="inline-flex items-center gap-2 px-5 py-3 text-sm font-bold rounded-xl bg-teal-600/10 text-teal-400 hover:bg-teal-600/20 transition-all border border-teal-600/20">
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
                Выписка из СРО
              </a>
            </div>
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

        <!-- Modal Content Container -->
        <div class="w-full h-full overflow-y-auto p-6 md:p-10 lg:p-16 bg-white relative flex flex-col">
          
          <!-- Text content -->
          <div class="w-full flex-grow">
            <h2 class="text-3xl sm:text-4xl lg:text-5xl font-black text-neutral-900 mb-8 lg:mb-10 leading-tight max-w-4xl">{{ selectedService.title }}</h2>
            
            <!-- Image -->
            <div class="w-full mb-8 sm:mb-10">
              <img v-if="selectedService.images && selectedService.images.length" :src="'/' + selectedService.images[0]" loading="lazy" class="w-full max-h-[250px] sm:max-h-[400px] lg:max-h-[500px] rounded-3xl object-cover shadow-xl" alt="Фото работ" />
            </div>

            <!-- Descriptive Text -->
            <div class="text-base sm:text-lg leading-relaxed text-neutral-600 max-w-none" v-html="selectedService.detailedDesc || selectedService.desc"></div>
          </div>

          <!-- Bottom CTA Button (Right aligned) -->
          <div class="mt-12 flex justify-end">
            <button
              @click="closeModalAndScrollToContact"
              class="w-full sm:w-auto px-10 py-5 text-lg font-bold rounded-xl bg-gradient-to-r from-teal-600 to-cyan-600 text-white shadow-xl shadow-teal-600/25 hover:shadow-teal-600/40 hover:-translate-y-1 transition-all duration-300"
            >
              Оставить заявку
            </button>
          </div>
          
        </div>

      </div>
    </div>
  </transition>
</template>
