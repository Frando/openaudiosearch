use crate::server::error::AppError;
use crate::State;
use oas_common::{types::Media, TypedValue};
use rocket::serde::json::Json;
use rocket_okapi::openapi;

use rocket::post;

/// Create a new feed
#[openapi(tag = "Task")]
#[post("/task/transcribe-media/<id>")]
pub async fn post_transcribe_media(
    state: &rocket::State<State>,
    id: String,
) -> Result<Json<String>, AppError> {
    let media = state.db.get_record::<Media>(&Media::guid(&id)).await?;
    match state.tasks.transcribe_media(&media).await {
        Ok(task_id) => Ok(Json(task_id)),
        Err(err) => Err(AppError::Other(format!("{}", err))),
    }
}
