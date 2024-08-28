<script>
import "../app.css";

const footerLinks = [
  {
    url: "/",
    title: "Back to the homepage",
    text: "Home",
  },
  {
    url: "/about/",
    title: "About Pitch Systems",
    text: "About",
  },
];
</script>

<div
  class="container mx-auto my-8 max-w-screen-md rounded-md bg-stone-50 p-6 shadow dark:bg-stone-900"
>
  <header class="py-8">
    <div
      class="p-6 text-center font-serif text-5xl text-emerald-900 dark:text-emerald-200"
    >
      Pitch Systems
    </div>
  </header>

  <main class="flex-grow">
    <slot></slot>         
  </main>

  <footer class="py-6">
    <nav>
      <ul class="flex list-none flex-row gap-x-4">
        {#each footerLinks as link}
          <li>
            <a href={link.url} title={link.title}>{link.text}</a>
          </li>
        {/each}
      </ul>
    </nav>
  </footer>
</div>
