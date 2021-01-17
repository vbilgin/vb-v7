const toggleIcon = document.querySelector('.nav__color-toggle')

let currentColorScheme = localStorage.getItem('colorScheme')

const setIconColor = (icon, colorScheme) => {
    if (colorScheme === 'light') {
        icon.setAttribute('fill', 'none')
        icon.setAttribute('stroke', '#0000ff')
    } else if (colorScheme === 'dark') {
        toggleIcon.setAttribute('fill', '#F6AE2D')
        toggleIcon.setAttribute('stroke', '#F6AE2D')
    }
}

const setInitialColorScheme = () => {
    if (!(document.documentElement.getAttribute('data-theme') === currentColorScheme)) {
        if (currentColorScheme === null || currentColorScheme === 'light') {
            document.documentElement.setAttribute('data-theme', 'light')
        } else if (currentColorScheme === 'dark') {
            document.documentElement.setAttribute('data-theme', 'dark')
            setIconColor(toggleIcon, 'dark')
        }
    } 
}

setInitialColorScheme()

toggleIcon.addEventListener('click', (e) => {
    currentColorScheme = localStorage.getItem('colorScheme')
    if (currentColorScheme === null || currentColorScheme === 'light') {
        document.documentElement.setAttribute('data-theme', 'dark')
        setIconColor(toggleIcon, 'dark')
        localStorage.setItem('colorScheme', 'dark')
    } else if (currentColorScheme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'light')
        localStorage.setItem('colorScheme', 'light')
        setIconColor(toggleIcon, 'light')
    }
})