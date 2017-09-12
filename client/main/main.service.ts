import { Injectable } from '@angular/core';
import { Http, Response, Headers } from '@angular/http';
import { JwtHttp } from 'angular2-jwt-refresh';

@Injectable()
export class MainService {
	constructor (private authHttp: JwtHttp) { }

	getApps() : Promise<string[]> {
		return this.authHttp.get(`/api/apps`)
			.toPromise()
			.then(this.extractData)
			.catch(this.handleError);
	}

	private extractData (res: Response) {
		let body = res.json();
		return body || {};
	}

	private handleError (error: Response | any): Promise<any> {
		let errMsg: string;
		let err: string;
		if (error instanceof Response) {
			const body = error.json() || '';
			err = body.error || body.detail || JSON.stringify(body);
			errMsg = `${error.status} - ${error.statusText || ''} ${err}`;
		} else {
			err = errMsg = error.message ? error.message : error.toString();
		}
		console.error(errMsg);
		throw new Error(err);
	}
}
