# -*- coding: utf-8 -*-
"""
Created on Thu May 13 17:18:34 2021

@author: Sergio Perea
"""

import cgi
# Headers
print("Content-Type: text/html")
print()



print("""<div class="container">
  <header class="header">
    <h1 id="title" class="text-center">COLECCIÓN SciELO.</h1>
    <p id="description" class="description text-center">
      REVISTAS CIENTÍFICAS ESPAÑOLAS DE CIENCIAS DE LA SALUD.
    </p>
  </header>
  <form id="survey-form" method="post" action="obtener_datos.py">
    <div class="form-group">
      <label id="name-label" for="name"></label>
      <input
        type="text"
        name="name"
        id="name"
        class="form-control"
        placeholder="Introduzca aquí su consulta..."
        required
      />
    </div>
  </form>
</div>""")

print("""<style type="text/css">
      :root {
  --color-white: #f3f3f3;
  --color-aqua: #00FFFF;
  --color-fuchsia: rgba(255,0,255, 0.8);
  --color-teal: #008080;
}

*,
*::before,
*::after {
  box-sizing: border-box;
}

body {
  font-family: 'Poppins', sans-serif;
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.4;
  color: var(--color-white);
  margin: 0;
}

/* mobile friendly alternative to using background-attachment: fixed */
body::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  z-index: -1;
  background: var(--color-aqua);
  background-image: linear-gradient(
      100deg,
      rgba(0,255,255, 0.8),
      rgba(136, 136, 206, 0.7)
    ),
    url(https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fimage.freepik.com%2Fvector-gratis%2Fcirculo-neon-efecto-luz-puntos-sobre-fondo-negro_106065-12.jpg&f=1&nofb=1);
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
}

h1 {
  font-weight: 400;
  line-height: 1.2;
}

p {
  font-size: 1.125rem;
}

h1,
p {
  margin-top: 0;
  margin-bottom: 0.5rem;
}

label {
  display: flex;
  align-items: center;
  font-size: 1.125rem;
  margin-bottom: 0.5rem;
}

input,
button,
select,
textarea {
  margin: 0;
  font-family: inherit;
  font-size: inherit;
  line-height: inherit;
}

button {
  border: none;
}

.container {
  width: 100%;
  margin: 3.125rem auto 0 auto;
}

@media (min-width: 576px) {
  .container {
    max-width: 540px;
  }
}

@media (min-width: 768px) {
  .container {
    max-width: 720px;
  }
}

.header {
  padding: 0 0.625rem;
  margin-bottom: 1.875rem;
}

.description {
  font-style: italic;
  font-weight: 200;
  text-shadow: 1px 1px 1px rgba(0, 0, 0, 0.4);
}

.clue {
  margin-left: 0.25rem;
  font-size: 0.9rem;
  color: #e4e4e4;
}

.text-center {
  text-align: center;
}

/* form */

form {
  background: var(--color-fuchsia);
  padding: 2.5rem 0.625rem;
  border-radius: 0.25rem;
}

@media (min-width: 480px) {
  form {
    padding: 2.5rem;
  }
}

.form-group {
  margin: 0 auto 1.25rem auto;
  padding: 0.25rem;
}

.form-control {
  display: block;
  width: 100%;
  height: 2.375rem;
  padding: 0.375rem 0.75rem;
  color: #495057;
  background-color: #fff;
  background-clip: padding-box;
  border: 1px solid #ced4da;
  border-radius: 0.25rem;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.form-control:focus {
  border-color: #80bdff;
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.input-radio,
.input-checkbox {
  display: inline-block;
  margin-right: 0.625rem;
  min-height: 1.25rem;
  min-width: 1.25rem;
}

.input-textarea {
  min-height: 120px;
  width: 100%;
  padding: 0.625rem;
  resize: vertical;
}

.submit-button {
  display: block;
  width: 100%;
  padding: 0.75rem;
  background: var(--color-teal);
  color: inherit;
  border-radius: 2px;
  cursor: pointer;
}

</style>""")