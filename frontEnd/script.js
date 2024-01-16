document.addEventListener('DOMContentLoaded', function() {
  fetch('http://localhost:5000/api/repositorios')
      .then(response => response.json())
      .then(data => mostrarRepositorios(data))
      .catch(error => console.error('Error:', error));
});

function mostrarRepositorios(repositorios) {
  const div = document.getElementById('repositorios');
  const lista = document.createElement('ul');

  repositorios.forEach(repo => {
      const item = document.createElement('li');
      item.innerHTML = `ID: ${repo.id}, ArtifactId: ${repo.artifactId}, GroupId: ${repo.groupId}, Repositorio: <a href="${repo.repositorio}">${repo.repositorio}</a>, Versión: ${repo.version}`;
      lista.appendChild(item);
  });

  div.appendChild(lista);
}
