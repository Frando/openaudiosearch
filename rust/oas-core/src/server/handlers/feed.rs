use crate::couch::types::{Doc, PutResponse};
use crate::server::error::AppError;
use crate::State;
use oas_common::Record;
use rocket::http::Status;
use rocket::serde::json::Json;
use rocket_okapi::{openapi, routes_with_openapi};

use oas_common::util;
use rocket::{get, post, put, routes, Route};

use oas_common::types;

/// Create a new feed
#[openapi(tag = "Feed")]
#[post("/feed", data = "<body>")]
pub async fn post_feed(
    state: &rocket::State<State>,
    body: Json<types::Feed>,
) -> Result<Json<PutResponse>, AppError> {
    // rocket::debug!("url: {}", body.into_inner().url);
    let feed = body.into_inner();
    let feed = Record::from_id_and_value(util::id_from_hashed_string(&feed.url), feed);
    let result = state.db.put_record(feed).await?;

    Ok(Json(result))
}

/// Put feed info by feed ID
#[openapi(tag = "Feed")]
#[put("/feed/<id>", data = "<body>")]
pub async fn put_feed(
    state: &rocket::State<State>,
    id: String,
    body: Json<types::Feed>,
) -> Result<Json<PutResponse>, AppError> {
    let feed = body.into_inner();
    let feed = Record::from_id_and_value(id, feed);
    let result = state.db.put_record(feed).await?;

    Ok(Json(result))
}

/// Get a feed by its id
#[openapi(tag = "Feed")]
#[get("/feed/<id>")]
pub async fn get_feed(
    state: &rocket::State<State>,
    id: String,
) -> Result<Json<Record<types::Feed>>, AppError> {
    let feed = state.db.get_record(&id).await?;
    Ok(Json(feed))
}
