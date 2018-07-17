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
    this.send('clear');
  }

  add(type, name, params) {
    this.send('add', name, Object.assign({type}, params));
  }

  update(name, params) {
    this.send('update', name, params);
  }
}

const ecran = new Ecran();
