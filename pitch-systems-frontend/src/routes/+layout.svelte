<script>
import "../app.css";

</script>

<div
  class="container relative mx-auto my-8 max-w-screen-md rounded-md bg-stone-50 p-6 shadow"
>
  <header class="py-8">
    <h1
      class="p-6 text-center font-serif text-5xl text-emerald-900"
    >
      Pitch Systems
  </h1>
  </header>

  <main class="flex-grow">
    <slot></slot>         
  </main>

  <footer class="py-6">

  </footer>
</div>
