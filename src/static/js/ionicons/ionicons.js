/*!
 * Ionicons v5.5.2 - Versión local simplificada
 * https://ionicons.com
 * MIT license: https://opensource.org/licenses/MIT
 */

(function() {
  // Definición de iconos básicos
  const defineCustomElement = function() {
    class IonIcon extends HTMLElement {
      constructor() {
        super();
        this.attachShadow({mode: 'open'});
      }
      
      connectedCallback() {
        this.render();
      }
      
      attributeChangedCallback() {
        this.render();
      }
      
      render() {
        const name = this.getAttribute('name');
        if (!name) return;
        
        // Renderizar el icono según el nombre
        this.shadowRoot.innerHTML = `
          <div style="display: inline-block; width: 1em; height: 1em;">
            <svg viewBox="0 0 512 512" style="width: 100%; height: 100%;">
              <path d="${this.getIconPath(name)}"></path>
            </svg>
          </div>
        `;
      }
      
      getIconPath(name) {
        // Aquí definimos algunos iconos básicos
        const icons = {
          'heart': 'M256 448l-30.164-27.211C118.718 322.442 48 258.61 48 179.095 48 114.221 97.918 64 162.4 64c36.399 0 70.717 16.742 93.6 43.947C278.882 80.742 313.199 64 349.6 64 414.082 64 464 114.221 464 179.095c0 79.516-70.719 143.348-177.836 241.694L256 448z',
          'star': 'M394 480a16 16 0 01-9.39-3L256 383.76 127.39 477a16 16 0 01-24.55-18.08L153 310.35 23 221.2a16 16 0 019-29.2h160.38l48.4-148.95a16 16 0 0130.44 0l48.4 149H480a16 16 0 019.05 29.2L359 310.35l50.13 148.53A16 16 0 01394 480z',
          'home': 'M261.56 101.28a8 8 0 00-11.06 0L66.4 277.15a8 8 0 00-2.47 5.79L63.9 448a32 32 0 0032 32H192a16 16 0 0016-16V328a8 8 0 018-8h80a8 8 0 018 8v136a16 16 0 0016 16h96.06a32 32 0 0032-32V282.94a8 8 0 00-2.47-5.79z',
          'person': 'M332.64 64.58C313.18 43.57 286 32 256 32c-30.16 0-57.43 11.5-76.8 32.38-19.58 21.11-29.12 49.8-26.88 80.78C156.76 206.28 203.27 256 256 256s99.16-49.71 103.67-110.82c2.27-30.7-7.33-59.33-27.03-80.6zM432 480H80a31 31 0 01-24.2-11.13c-6.5-7.77-9.12-18.38-7.18-29.11C57.06 392.94 83.4 353.61 124.8 326c36.78-24.51 83.37-38 131.2-38s94.42 13.5 131.2 38c41.4 27.6 67.74 66.93 76.18 113.75 1.94 10.73-.68 21.34-7.18 29.11A31 31 0 01432 480z',
          'search': 'M456.69 421.39L362.6 327.3a173.81 173.81 0 0034.84-104.58C397.44 126.38 319.06 48 222.72 48S48 126.38 48 222.72s78.38 174.72 174.72 174.72A173.81 173.81 0 00327.3 362.6l94.09 94.09a25 25 0 0035.3-35.3zM97.92 222.72a124.8 124.8 0 11124.8 124.8 124.95 124.95 0 01-124.8-124.8z'
        };
        
        return icons[name] || '';
      }
      
      static get observedAttributes() {
        return ['name', 'color', 'size'];
      }
    }
    
    if (!customElements.get('ion-icon')) {
      customElements.define('ion-icon', IonIcon);
    }
  };
  
  // Ejecutar la definición
  defineCustomElement();
})();
