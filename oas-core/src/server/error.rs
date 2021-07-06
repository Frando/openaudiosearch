use oas_common::types::{AudioObject, Feed};
use oas_common::{DecodingError, Record, TypedValue, UntypedRecord};
use rocket::http::Status;
use rocket::response::status::Custom;
use rocket::response::{status, Responder};
use rocket::{get, post, put, response, response::content, routes, Request, Route};
use serde::Serialize;
use serde_json::{json, Value};
use thiserror::Error;

use crate::couch::{CouchError, Doc};
pub type Result<T> = std::result::Result<rocket::serde::json::Json<T>, AppError>;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("{0}")]
    DecodingError(#[from] DecodingError),
    #[error("{0}")]
    Couch(#[from] CouchError),
    #[error("{0}")]
    Serde(#[from] serde_json::Error),
    #[error("{0}")]
    Other(String),
}

impl<'r> Responder<'r, 'static> for AppError {
    fn respond_to(self, req: &'r Request<'_>) -> response::Result<'static> {
        let json = json!({ "error": format!("{}", self) });
        let string = serde_json::to_string(&json).unwrap();
        let code = match self {
            // TODO: Change to 500
            AppError::Couch(_err) => Status::BadGateway,
            _ => Status::InternalServerError,
        };
        Custom(code, content::Json(string)).respond_to(req)
    }
}
