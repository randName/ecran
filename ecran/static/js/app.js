class Ecran {
  constructor() {
  }

  send(action, name, params) {
    let data = {action, name, params}
    return fetch('canvas', {
      mode: 'cors', method: 'POST',
      body: JSON.stringify(data),
      headers: {'content-type': 'application/json'}
    }).then(r => r.json());
  }

  clear() {
    return this.send('clear');
  }

  add(type, name, params) {
    return this.send('add', name, Object.assign({type}, params));
  }

  update(name, params) {
    return this.send('update', name, params);
  }

  shutdown() {
    fetch('shutdown');
  }

  reload() {
    fetch('reload');
  }
}

const ecran = new Ecran();
